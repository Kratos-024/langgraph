from dotenv import load_dotenv
load_dotenv(".env")

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

base_llm = HuggingFaceEndpoint(
    model="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=50,
    do_sample=False,
)

chat_llm = ChatHuggingFace(llm=base_llm)

response = chat_llm.invoke("what is a dog?")
print(response.content)
