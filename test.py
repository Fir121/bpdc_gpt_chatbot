import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import QuestionAnswerPrompt, GPTVectorStoreIndex
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig, LlamaIndexTool
from langchain.chat_models import ChatOpenAI

index = GPTVectorStoreIndex.load_from_disk(f'Annual Reports.json')
r = index.query("What are some of the events ACM conducted in 2018-19")
print(r)