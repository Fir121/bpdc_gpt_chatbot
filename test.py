import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import QuestionAnswerPrompt, GPTVectorStoreIndex, LLMPredictor, ServiceContext, GPTListIndex
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig, LlamaIndexTool, GraphToolConfig
from langchain.chat_models import ChatOpenAI
from llama_index.indices.composability import ComposableGraph
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform


# Load indices from disk
index_set = {}
datas = ["FAQ2", "Wiki"]
for d in datas:
    cur_index = GPTVectorStoreIndex.load_from_disk(f'{d}.json')
    index_set[d] = cur_index

# make far more detailed descriptions so much more segregated data
index_summaries = [
                    "Collection of common answers related to the internal workings at BPDC with details about the BPDC Library, Icebreakers, Clubs and associations such as Sports Club, Trebel, ACM, MTC, WSC Groove, CIIED, WIE, Toastmasters, Chimera, Creative Lab, Shades, The Editorial Board, Allure, Flummoxed Quizzing Club, AIChE, Paribhasha, MAD Club, Reflections, IFOR, EMC, Guild. and Events such as Jashn, BSF, IceBreakers etc.",
                    "Overview of Bits Pilani Dubai Campus and extract from the Wikipedia. Has information on the history, academics, student life and culture, notable alumni, references and more"
                ]

# define toolkit
index_configs = []
i = 0
for y in datas:
    tool_config = IndexToolConfig(
        index=index_set[y], 
        name=f"Vector Index {y}",
        description=index_summaries[i],
        tool_kwargs={"return_direct": True, "return_sources": True},
    )
    index_configs.append(tool_config)
    i += 1

toolkit = LlamaToolkit(
    index_configs=index_configs
)



memory = ConversationBufferMemory(memory_key="chat_history")
llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")
agent_chain = create_llama_chat_agent(
    toolkit,
    llm,
    memory=memory,
    verbose=True
)

while True:
    text_input = input("User: ")
    # handle valueerror
    response = agent_chain.run(input=text_input)
    print(f'Agent: {response}')

