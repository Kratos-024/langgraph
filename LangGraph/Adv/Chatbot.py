import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
import psycopg
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessageChunk, BaseMessage

load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    streaming=True  
)
model = ChatHuggingFace(llm=llm)

class Messages_State(TypedDict):
    message_history: Annotated[List[BaseMessage], add_messages]

def chatBot(state: Messages_State):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a teacher. Answer the question asked by student."),
        MessagesPlaceholder(variable_name="message_history"),
    ])

    prompt = prompt_template.invoke({'message_history': state['message_history']})
    response = model.invoke(prompt)

    return {"message_history": [response]}

DB_URI = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"

pool = ConnectionPool(conninfo=DB_URI, kwargs={"autocommit": True})

checkpointer = PostgresSaver(pool)
checkpointer.setup()

builder = StateGraph(Messages_State)
builder.add_node("chatBot", chatBot)
builder.add_edge(START, 'chatBot')
builder.add_edge('chatBot', END)

workflow = builder.compile(checkpointer=checkpointer)

def startStream(user_query: str, thread_id: str = "1"):
    input_data = {'message_history': [HumanMessage(content=user_query)]}
    config = {'configurable': {'thread_id': thread_id}}
    
    for msg, metadata in workflow.stream(input_data, config=config, stream_mode="messages"):
        if isinstance(msg, AIMessageChunk):
            yield msg.content

def getSessions():
    unique_ids = list({t.config["configurable"]["thread_id"] for t in checkpointer.list(config={})})
    return unique_ids

def getChats(thread_id: str):
    config = {'configurable': {'thread_id': thread_id}}
    threads = checkpointer.list(config=config)
    chats = []
    
    for i in threads:
        history = i.checkpoint['channel_values']['message_history']
        for j in history:
            is_user = isinstance(j, HumanMessage)
            chats.append({
                "content": j.content,
                "isUser": is_user
            })
        break

    return chats