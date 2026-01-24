from langgraph.graph import StateGraph, START , END
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict,Optional, Annotated,List
from  langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from  langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from  langchain_core.messages import HumanMessage,AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages



class Messages_State(TypedDict):
    message_history : Annotated[List[BaseMessage],add_messages]

     
llm = HuggingFaceEndpoint(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    streaming=True  
)
model = ChatHuggingFace(llm=llm)
def chatBot(state:Messages_State):
    message = state['message_history'][-1]
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a teacher. Answer the question asked by student."),
       MessagesPlaceholder(variable_name="chat_history"), ("human", "{message}")
    ])

    prompt = template.invoke({'message':message.content, 'chat_history':state['message_history'][:-1]})

    result = model.invoke(prompt)

    return {
    "message_history": [result]
}

graph = StateGraph(Messages_State)
checkpointer = MemorySaver()
from langchain_core.messages import AIMessageChunk

graph.add_node("chatBot",chatBot)
graph.add_edge(START,'chatBot')
graph.add_edge('chatBot',END)
workflow = graph.compile(checkpointer=checkpointer)


# def startSession(user_query):
#     thread_id = '1'
#     startSession2(user_query)
#     user_query = HumanMessage(content=user_query)
#     config = {'configurable': {'thread_id': thread_id}}
#     result =  workflow.invoke({'message_history':[user_query]}, config=config)

#     last_message = result['message_history'][-1]

#     if isinstance(last_message, AIMessage):
#         return last_message.content
#     else:
#         return str(last_message)


def startSession2(user_query):
    thread_id = '2'
    user_query = HumanMessage(content=user_query)
    config = {'configurable': {'thread_id': thread_id}}
    
    for msg, metadata in workflow.stream({'message_history':[user_query]}, config=config, stream_mode="messages"):
        if isinstance(msg, AIMessageChunk):
            yield (msg.content)