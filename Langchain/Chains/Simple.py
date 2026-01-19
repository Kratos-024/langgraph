from langchain_core import prompts
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv('.env')

promptTemplate1 = prompts.PromptTemplate(template=
                                         """Write something about this topic {topic}""",
                                        input_variables=['topic'],validate_template=True)

promptTemplate2  = prompts.PromptTemplate(template=
                                         """Get 1 point from this text {text}""",
                                        input_variables=['text'],validate_template=True)



llm = HuggingFaceEndpoint(model="deepseek-ai/DeepSeek-R1",
    task="text-generation",
    max_new_tokens=50,
   )
model = ChatHuggingFace(llm=llm)
outputParser = StrOutputParser()
 
chain = promptTemplate1 | model | outputParser | promptTemplate2 | model | outputParser

result = chain.invoke({'topic':"Black hole"})


print(result)




