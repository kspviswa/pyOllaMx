from mlxLLM import MlxLLM
from search import *
#from mlxLLM_local import MlxLLM_local
import requests
from ollamaClient import OllamaClient
from mlxClient import MlxClient

oChatClient = OllamaClient()
oSearchClient = OllamaClient()

mChatClient = MlxClient()
mSearchClient = MlxClient()

def doOllamaChat(client, prompt: str, model: str, temp: float, system:str ='default'):
    response = client.chat(prompt=prompt, model=model, temp=temp, system=system)
    return response

def doOllamaChatStream(client, prompt: str, model: str, temp: float, system:str='default'):
    response = client.chat_stream(prompt=prompt, model=model, temp=temp, system=system)
    return response

def clearClientHistory(client):
    client.clear_history()

def clearAllHistory():
    oChatClient.clear_history()
    oSearchClient.clear_history()
    mChatClient.clear_history()
    mSearchClient.clear_history()

def clearChatHistory():
    clearClientHistory(oChatClient)
    clearClientHistory(mChatClient)

def clearSearchHistory():
    clearClientHistory(oSearchClient)
    clearClientHistory(mSearchClient)

def appendHistoryforOllamaChatStream(client, message):
    client.append_history(message)

def firePrompt(prompt: str, model: str="dolphin-mistral:latest", temp=0.4, isMlx=False, chat_mode=False, system:str = 'default') :
    response, keywords = "", ""
    if chat_mode:
        llm = mChatClient if isMlx else oChatClient
        try:
            response = llm.chat(model=model, temp=temp, prompt=prompt, system=system)
        except requests.exceptions.ConnectionError as e:
            err_str = f'PyOMlX' if isMlx else f'Ollama'
            return f'Unable to connect to {err_str}. Is it running?🤔', ""
        except Exception as e:
            return f'Generic Error Occured {e}', ""
        
    else :
        llm = mSearchClient if isMlx else oSearchClient
        # First summarize the user prompt into keywords
        try:
            keyprompt = wrapPromptWithSearch_str(prompt)
            keywords = llm.chat(model=model, temp=temp, prompt=keyprompt, system=getKeywordSystemPrompt())
            #print(f'Keywords : {keywords}')
            # Do websearch with keywords
            search_results = doWebSearch(keywords)
            #print(f'Search result : {search_results}')
            # Do a RAG with search_results with LLM
            final_prompt = decorateSearchPrompt(search_results, prompt)
            response = llm.chat(model=model, temp=temp, prompt=final_prompt, system=getSearchSystemPrompt())
        except requests.exceptions.ConnectionError as e:
            err_str = f'PyOMlX' if isMlx else f'Ollama'
            return f'Unable to connect to {err_str}. Is it running?🤔', ""
        except Exception as e:
            return f'Generic Error Occured {e}', ""
        
    return response, keywords





# def firePrompt1(prompt: str, model: str="dolphin-mistral:latest", temp=0.4, isMlx=False, chat_mode=False) -> str:
#     res = ""
#     keywords = ""
#     if chat_mode:
#         if isMlx:
#             llm = MlxLLM(model=model, temp=temp)
#             #llm = OllamaClient()
#             #llm = MlxLLM_local(model=model, temp=temp)
#         else:
#             #llm = Ollama(model=model,
#             #    temperature=temp
#             #    )
#             llm = OllamaClient()
#         try:
#             #res = llm.invoke(prompt)
#             res = llm.chat(model=model, temp=temp, prompt=prompt)
#         except requests.exceptions.ConnectionError as e:
#             err_str = f'PyOMlX' if isMlx else f'Ollama'
#             return f'Unable to connect to {err_str}. Is it running?🤔', ""
#         except Exception as e:
#             return f'Generic Error Occured {e}', ""
#     else:
#         try:
#             if isMlx:
#                 res = f'Search not implemented for MlX models. Stay tuned!'
#             else:
#                 res, keywords = retSearchResults(model=model, search_str=prompt, temp=temp)
#         except Exception as e:
#             return f'__Generic Error Occured__ {e}', ""
#     return res, keywords