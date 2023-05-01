import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import GPTVectorStoreIndex, QuestionAnswerPrompt
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
from langchain.chat_models import ChatOpenAI
import time, pickle

# Load indices from disk
index_set = {}
datas = ["FAQ", "Wiki", "About","Program Information", "Fees and Scholarships", "Visa Information", "Career","Clubs","Other FAQ"]
for d in datas:
    cur_index = GPTVectorStoreIndex.load_from_disk(f'{d}.json')
    index_set[d] = cur_index

# make far more detailed descriptions so much more segregated data
index_summaries = [
                    "Collection of common answers related to the internal workings at BPDC with details about the BPDC Library, WebOPAC portal, Question Papers. And Events such as BSF, IceBreakers etc.",
                    "Overview of Bits Pilani Dubai Campus and extract from the Wikipedia. Has information on the director, chancellor, vice chancellor, campus size and location, campus affiliations, overview, history, campus and DIAC (Dubai International Academic City), Hostels, Labs, Departments, Practice School (PS 1 AND 2), Events, DIAC Residential Halls, and notable alumni",
                    "Simple description About Bits Pilani Dubai extracted from the BPDC Website including Mission, Vision, Policy and a general overview",
                    "Detailed Information on all the degree programs at BPDC and their respective admission criteria. Includes details on Bachelor Of Engineering (First Degree), Master Of Engineering (Higher Degree), MBA, PhD programs",
                    "All details about the fee structure, scholarships, payment plan, concessions etc. for the degree programs (First and Higher) at BPDC",
                    "Details about UAE Residence Visa which is required to study at BPDC, how to apply and get this visa",
                    "All about careers and placements at BPDC, in depth information about the Practice School (PS) program at BPDC",
                    "Details on all the clubs, associations and chapters at BPDC, with details on clubs such as Sports, Scientific Associations, Cultural Activites, MAD (social and environmental club making a difference), public speaking and literary, dance club (groove), drama club (paribasha), art club (shades), music club (trebel), design club, fashion club (allure), photography club (reflexions), quiz club (flummoxed), supernova (astronomy), wall street club, ieee, acm and sae chapters",
                    "More commonly asked questions about BPDC related to Admissions, Fees, Hostel, Visa, and other including transfers, visa, costs, dress code, insurance, prospects and more"
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

QA_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given the context information and common sense, and chat history but not prior knowledge"
    "answer the question. If you don't know the answer, reply 'I don't know': {query_str}\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

def return_chain(memory):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    agent_chain = create_llama_chat_agent(
        toolkit,
        llm,
        memory=memory,
        verbose=True,
        text_qa_template=QA_PROMPT
    )
    return agent_chain

def create_chain():
    memory = ConversationBufferMemory(memory_key="chat_history")
    agc = return_chain(memory)
    fname = f"{time.time()}.pkl"
    with open("memorychains/"+fname,"wb") as f:
        pickle.dump(agc.memory,f)
    return agc, fname

def save_chain(chain, fname):
    with open("memorychains/"+fname,"wb") as f:
        pickle.dump(chain.memory,f)

def load_chain(fname):
    with open("memorychains/"+fname,"rb") as f:
        memory = pickle.load(f)
    return return_chain(memory)

def none_parser(dataDict):
    for d in dataDict:
        if dataDict[d] == 'None':
            dataDict[d] = None
    return dataDict

