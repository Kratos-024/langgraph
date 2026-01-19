from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv('.env')


prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a short 10 line story about the topic provided."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{topic}"),
])

llm = HuggingFaceEndpoint(
    model="deepseek-ai/DeepSeek-V3",
    task="text-generation",
    max_new_tokens=512
)
chat_llm = ChatHuggingFace(llm=llm)

chain = prompt | chat_llm

demo_ephemeral_chat_history_for_session = {}

def get_session_history(session_id: str):
    if session_id not in demo_ephemeral_chat_history_for_session:
        demo_ephemeral_chat_history_for_session[session_id] = ChatMessageHistory()
    return demo_ephemeral_chat_history_for_session[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="topic",
    history_messages_key="chat_history",
)


result = chain_with_history.invoke(
    {"topic": "Kung Fu Panda"},
    config={"configurable": {"session_id": "user_1"}}
)

print(result.content)