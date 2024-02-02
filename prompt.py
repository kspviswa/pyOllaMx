from langchain_community.llms import Ollama
#from langchain_community.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
#from  langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
#from langchain.agents import AgentExecutor, create_react_agent, create_self_ask_with_search_agent
#from langchain_core.tools import Tool
#from langchain import hub
from mlxLLM import MlxLLM


#tools = [DuckDuckGoSearchRun(name='Intermediate Answer')]

def firePrompt(prompt: str, model: str="dolphin-mistral:latest", temp=0.4, isMlx=False) -> str:
    if isMlx:
        llm = MlxLLM(model=model, temp=temp)
    else:
        llm = Ollama(model=model,
             temperature=temp
             )
    #agent = create_self_ask_with_search_agent(llm=llm, tools=tools, prompt=hub.pull("hwchase17/self-ask-with-search"))
    #agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    #res = agent_executor.invoke({"input" : prompt})
    #return res['output']
    res = llm.invoke(prompt)
    return res