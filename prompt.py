from langchain_community.llms import Ollama
from mlxLLM import MlxLLM
from search import retSearchResults
#from mlxLLM_local import MlxLLM_local
import requests

def firePrompt(prompt: str, model: str="dolphin-mistral:latest", temp=0.4, isMlx=False, chat_mode=False) -> str:
    res = ""
    keywords = ""
    if chat_mode:
        if isMlx:
            llm = MlxLLM(model=model, temp=temp)
            #llm = MlxLLM_local(model=model, temp=temp)
        else:
            llm = Ollama(model=model,
                temperature=temp
                )
        try:
            res = llm.invoke(prompt)
        except requests.exceptions.ConnectionError as e:
            err_str = f'PyOMlX' if isMlx else f'Ollama'
            return f'Unable to connect to {err_str}. Is it running?🤔', ""
        except Exception as e:
            return f'Generic Error Occured {e}', ""
    else:
        try:
            if isMlx:
                res = f'Search not implemented for MlX models. Stay tuned!'
            else:
                res, keywords = retSearchResults(model=model, search_str=prompt, temp=temp)
        except Exception as e:
            return f'__Generic Error Occured__ {e}', ""
    return res, keywords