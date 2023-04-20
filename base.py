import constants
import os
os.environ["OPENAI_API_KEY"] = constants.openapi_key


from llama_index import GPTSimpleVectorIndex
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
from langchain.chat_models import ChatOpenAI

index = GPTSimpleVectorIndex.load_from_disk('index.json')
indexes = [
    IndexToolConfig(
            index=index, 
            name="Vector Index",
            description="useful for when you want to answer queries about ACM",
            index_query_kwargs={"similarity_top_k": 3},
            tool_kwargs={"return_direct": True}
    )
]
toolkit = LlamaToolkit(
    index_configs=indexes
)

memory = ConversationBufferMemory(memory_key="chat_history")
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
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