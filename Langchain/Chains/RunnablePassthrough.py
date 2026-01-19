from itertools import chain
from langchain_core import prompts
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
load_dotenv('.env')

promptTemplate1 = prompts.PromptTemplate(template=
                                         """Tell me 5 superheros name from this {topic}""",
                                        input_variables=['topic'],validate_template=True)


promptTemplate2  = prompts.PromptTemplate(template=
                                         """Who is the weakest one from these {text}""",
                                        input_variables=['text'],validate_template=True)


promptTemplate3  = prompts.PromptTemplate(template=
                                         """Tell me only Who is he/she {text2} and nothing else i said nothing else should be written except who is he/she""",
                                        input_variables=['text2'],validate_template=True)



llm = HuggingFaceEndpoint(model="deepseek-ai/DeepSeek-R1",
    task="text-generation",
    max_new_tokens=50,
   )
model = ChatHuggingFace(llm=llm)
outputParser = StrOutputParser()

chain = promptTemplate1 | model | outputParser

parallel_chain = RunnableSequence(
     promptTemplate2 |  model |outputParser,
     promptTemplate3 | model | outputParser
)
merge_chain = chain | parallel_chain 
result  = merge_chain.invoke({'topic':"Avengers"})


print(result)




