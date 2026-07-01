def retrieve_context(query, retriever):

    docs = retriever.get_relevant_documents(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    return context, docs