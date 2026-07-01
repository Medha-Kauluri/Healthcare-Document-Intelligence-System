import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

from agents.retrieval_agent import retrieve_context

from agents.summary_agent import summarize_document
from agents.disease_agent import explain_disease
#from agents.treatment_agent import treatment_summary
from agents.risk_agent import risk_analysis
from agents.patient_agent import patient_explanation

load_dotenv()

if "processed" not in st.session_state:
    st.session_state.processed = False

st.set_page_config(
    page_title="Healthcare Document Intelligence System",
    layout="wide"
)

st.title("🏥 Healthcare Document Intelligence System")
st.markdown(
    "LLMs + RAG + Medical Document Analysis"
)

with st.sidebar:

    st.header("Healthcare AI Agents")

    st.write("📄 Summary Agent")
    st.write("🩺 Disease Agent")
    # st.write("💊 Treatment Agent")
    st.write("⚠️ Clinical Insights Agent")
    st.write("👨‍⚕️ Patient Explanation Agent")

    analysis_type = st.selectbox(
    "Select Analysis",
    [
        "Summary",
        "Disease Analysis",
        "Clinical Insights",
        "Patient Explanation"
    ]
)
    document_type = st.selectbox(
        "Document Type",
        [
            "Medical Report",
            "Research Paper",
            "Lab Report"
        ]
    )

uploaded_file = st.file_uploader(
    "Upload Medical Report / Research Paper",
    type="pdf"
)

if uploaded_file:

    st.success("PDF Uploaded Successfully")

    if st.button("Process Document"):

        with st.spinner("Processing Document..."):

            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            loader = PyPDFLoader("temp.pdf")

            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            docs = splitter.split_documents(
                documents
            )

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            vectorstore = FAISS.from_documents(
                docs,
                embeddings
            )

            st.session_state.retriever = (
                vectorstore.as_retriever(
                    search_kwargs={"k": 8}
                )
            )

            st.session_state.llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                api_key=os.getenv(
                    "GROQ_API_KEY"
                )
            )

            st.session_state.processed = True

        st.success(
            "Document Processed Successfully!"
        )

if st.session_state.processed:

    query = st.text_input(
        "Ask a question about the document"
    )

    if st.button("Analyze"):

        if query.strip() == "":
            query = "Analyze the document"

        with st.spinner(
            "Running Healthcare Intelligence System..."
        ):

            context, relevant_docs = retrieve_context(
                query,
                st.session_state.retriever
            )

            if analysis_type == "Summary":

                result = summarize_document(
                    st.session_state.llm,
                    context
                )

            elif analysis_type == "Disease Explanation":

                result = explain_disease(
                    st.session_state.llm,
                    context
                )

            #elif analysis_type == "Treatment Summary":

            # result = treatment_summary(
                #    st.session_state.llm,
                #   context)

            elif analysis_type == "Clinical Insights":

                result = risk_analysis(
                    st.session_state.llm,
                    context
                )

            else:

                result = patient_explanation(
                    st.session_state.llm,
                    context
                )

        st.divider()

        st.subheader(
            "Healthcare Intelligence Output"
        )

        st.write(result)

        st.divider()

        st.subheader(
            "Evidence Retrieved"
        )

        for i, doc in enumerate(relevant_docs):

            with st.expander(
                f"Source Chunk {i+1}"
            ):
                st.write(
                    doc.page_content
                )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Retrieved Chunks",
                len(relevant_docs)
            )

        with col2:

            st.metric(
                "Document Sources",
                len(relevant_docs)
            )