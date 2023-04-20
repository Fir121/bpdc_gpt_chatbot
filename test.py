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
datas = ["Annual Reports", "Careers", "FAQ", "General Information"]
for d in datas:
    cur_index = GPTVectorStoreIndex.load_from_disk(f'{d}.json')
    index_set[d] = cur_index

index_summaries = [
                    "Collection of all the Annual Reports of ACM BPDC Over the last 10 academic years ranging from 2010-2022",
                    "List of positions available in the ACM Council, their descriptions, requirements and conditions",
                    "List of frequently asked questions by ACM members about ACM events, workshops, membership and more",
                    "General Information about the ACM BPDC Student Chapter"
                ]

# set number of output tokens
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, max_tokens=3982, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
graph = ComposableGraph.load_from_disk('datas.json', service_context=service_context)

decompose_transform = DecomposeQueryTransform(
    llm_predictor, verbose=True
)

query_configs = [
    {
        "index_struct_type": "simple_dict",
        "query_mode": "default",
        "query_kwargs": {
            "similarity_top_k": 1,
            # "include_summary": True
        },
        "query_transform": decompose_transform
    },
    {
        "index_struct_type": "list",
        "query_mode": "default",
        "query_kwargs": {
            "response_mode": "tree_summarize",
            "verbose": True
        }
    },
]



# define toolkit
index_configs = []
i = 0
for y in datas:
    tool_config = IndexToolConfig(
        index=index_set[y], 
        name=f"Vector Index {y}",
        description=index_summaries[i],
        index_query_kwargs={"similarity_top_k": 3},
        tool_kwargs={"return_direct": True, "return_sources": True},
    )
    index_configs.append(tool_config)
    i += 1
    
# graph config
graph_config = GraphToolConfig(
    graph=graph,
    name=f"Graph Index",
    description="useful for when you want to answer queries that require analyzing information about different parts of ACM",
    query_configs=query_configs,
    tool_kwargs={"return_direct": True, "return_sources": True},
    return_sources=True
)

toolkit = LlamaToolkit(
    index_configs=index_configs,
    graph_configs=[graph_config]
)


QA_PROMPT_TMPL = (
    "Below is some information about ACM BPDC. This information was extracted using a language model, so it may be of varied accuracy. Using this and the question please come up with an accurate and relevant answer \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Please answer the question: {query_str}\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

memory = ConversationBufferMemory(memory_key="chat_history")
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

