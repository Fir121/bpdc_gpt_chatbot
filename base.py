import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import QuestionAnswerPrompt, GPTVectorStoreIndex
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig, LlamaIndexTool
from langchain.chat_models import ChatOpenAI
import pickle

# try instead keywordindex
# use custom QuestionAnswerPrompt
dirs = os.listdir("data")
idxc = []
for d in dirs:
    index = GPTVectorStoreIndex.load_from_disk(f'{d}.json')
    tool_config = IndexToolConfig(
                    index=index, 
                    name=f"{d} Vector Index",
                    description= str(index.query("What is a summary of these documents?")),
            )
    idxc.append(tool_config)

toolkit = LlamaToolkit(
    index_configs=idxc
)

QA_PROMPT_TMPL = (
    "Below is some information about ACM BPDC. This information was extracted using a language model, so it may be of varied accuracy. Using this and the question please come up with an accurate and relevant answer \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Please answer the question: {query_str}\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)


with open("saveddata.json","rb") as f:
    memory = pickle.load(f)
#memory = ConversationBufferMemory(memory_key="chat_history")
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
agent_chain = create_llama_chat_agent(
    toolkit,
    llm,
    memory=memory,
    verbose=True,
    text_qa_template=QA_PROMPT
)


response = agent_chain.run(input="You are a chatbot for the ACM student chapter at Bits Pilani, Dubai Campus (BPDC). Your name is ACM-Assistant. You must assist the user in any way possible. If available, you will be provided with certain context information that you must use to enhance your responses.")
print(f'Agent: {response}')
while True:
    text_input = input("User: ")
    # handle valueerror
    response = agent_chain.run(input=text_input)
    print(f'Agent: {response}')