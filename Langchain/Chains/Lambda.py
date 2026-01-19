from langchain_core import prompts
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from dotenv import load_dotenv

load_dotenv('.env')

promptTemplate1 = prompts.PromptTemplate(
    template="Tell me 5 superheroes from this {topic}",
    input_variables=['topic'],
    validate_template=True
)

promptTemplate2 = prompts.PromptTemplate(
    template="Who is the weakest one from these {text}",
    input_variables=['text'],
    validate_template=True
)

promptTemplate3 = prompts.PromptTemplate(
    template="Tell me only who is he/she {text2} and nothing else",
    input_variables=['text2'],
    validate_template=True
)

llm = HuggingFaceEndpoint(model="deepseek-ai/DeepSeek-R1",
                          task="text-generation",
                          max_new_tokens=50)
model = ChatHuggingFace(llm=llm)
outputParser = StrOutputParser()

hero_chain = RunnableSequence(promptTemplate1, model, outputParser)

parallel_chain = RunnableParallel({
    'Heroes': RunnableLambda(lambda x: x),             
    'WordCount': RunnableLambda(lambda x: len(x.split()))   
})

extract_heroes = RunnableLambda(lambda d: {'text': d['Heroes']})

weakest_chain = RunnableSequence(
    extract_heroes,
    promptTemplate2,
    model,
    outputParser
)

final_description = RunnableSequence(
    RunnableLambda(lambda x: {'text2': x}), 
    promptTemplate3,
    model,
    outputParser
)

full_chain = RunnableSequence(
    hero_chain,
    parallel_chain,
    weakest_chain,
    final_description
)

result = full_chain.invoke({'topic': 'Avengers'})
print(result)
