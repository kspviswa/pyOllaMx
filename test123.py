from langchain_community.utilities import SearxSearchWrapper

searchNxg = SearxSearchWrapper(searx_host="https://searx.sev.monster/")
searchResults = searchNxg.run("What is searXNG?")
print(searchResults)