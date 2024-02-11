from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

wrapper = DuckDuckGoSearchAPIWrapper(time="d", max_results=3)
search = DuckDuckGoSearchResults(api_wrapper=wrapper)

search_prompt = f"""
    You are a helpful assistant capable of performing a web research. If the user_prompt is not an instruction, task or question, donot proceed to summarize. Instead, politely request the user that you cannot engage in general chat. If not, Use the information available in search_text to summarize an answer for the the user_prompt. While generating the summary, cite the sources from the search_text by converting the citation as a hyperlink using markdown format. 

    search_text : 
    user_prompt :
"""

keyword_prompt = f"""
    Just summarize the input_text into few keywords. Don't respond other than the summary .
"""

chat_history = []

def retPrompt(res, up):
    tprompt = f"""
    search_text : {res}
    user_prompt : {up}
    """
    return tprompt

def retSearchResults(model: str = "", search_str: str = "") -> str:
    keywords_llm = Ollama(model=model, system=keyword_prompt)
    query_str = keywords_llm.invoke(f'input_text : \n {search_str}')
    print(f'Keywords for this search texts are {query_str}')
    search_llm = Ollama(model=model, system=search_prompt)
    searchResults = search.run(query_str)
    response = search_llm.invoke(retPrompt(searchResults, search_str))
    return response, query_str
