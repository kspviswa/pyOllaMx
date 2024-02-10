from llama_index import ServiceContext
from llama_index.llms import Ollama

import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index import StorageContext
import re



def extract_urls(text):
    url_pattern = re.compile(r'link: (https?://[^\s,]+)')
    urls = re.findall(url_pattern, text)
    return urls

from langchain_community.tools import DuckDuckGoSearchResults
search = DuckDuckGoSearchResults()
result = search.run("What is catch-up contribution?")
results = extract_urls(result)
parsed_results = []
for r in results:
    parsed_results.append(r.replace("]",""))

print(parsed_results)

chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.create_collection(name="ddg", get_or_create=True)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
from llama_index import VectorStoreIndex
from llama_index.readers import SimpleWebPageReader
documents = SimpleWebPageReader(html_to_text=True).load_data(
    parsed_results
)

llm1 = Ollama(model="dolphin-mistral:latest")
service_context = ServiceContext.from_defaults(llm=llm1, embed_model='local')

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)
query_engine = index.as_query_engine()
response = query_engine.query("What is catch-up contribution?")
#print(response)
print(response.source_nodes)

