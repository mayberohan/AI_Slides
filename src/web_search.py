def search_web(query):
    """
    Mock web search function.
    Always returns simple placeholder results for the given query.
    """
    print(f"🔍 Mock searching for: {query}")
    return [
        f"{query} overview and introduction.",
        f"Key challenges related to {query}.",
        f"Recent developments in {query}.",
        f"Case studies/examples of {query}.",
        f"Future outlook on {query}."
    ]
