from dotenv import load_dotenv
load_dotenv('../.env')
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite', 
    api_key='AIzaSyAr66ZFYbAV4ur91gqKYM3T8G6ZiKxcqQs',max_output_tokens= 12,
)
result = llm.invoke('what is dog?')
print(result.content)

