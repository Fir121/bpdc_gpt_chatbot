import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex


dirs = os.listdir("data")
for d in dirs:
    documents = SimpleDirectoryReader(f'data/{d}').load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.save_to_disk(f'{d}.json')

