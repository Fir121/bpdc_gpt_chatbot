import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex.from_documents(documents)
index.save_to_disk('index.json')
