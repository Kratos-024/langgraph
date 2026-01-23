from langchain_huggingface import HuggingFaceEmbeddings
import sklearn.metrics.pairwise as cs 
from torch import embedding
import numpy as np

with open('harrypotter.txt','r',encoding='utf-8') as f:
    doc = f.read()
doc = doc.split(',')
docc = [
    "Harry Potter was a young wizard who lived with his aunt and uncle.",
    "He received a letter inviting him to attend Hogwarts School of Witchcraft and Wizardry.",
    "At Hogwarts, Harry made friends like Ron Weasley and Hermione Granger.",
    "The school was full of magical creatures, enchanted objects, and secret passages.",
    "Harry discovered he was famous in the wizarding world for surviving an attack by Voldemort as a baby.",
    "Throughout the years, he faced various challenges, including potions, spells, and dangerous creatures.",
    "Quidditch was a favorite sport of Harry and his friends at Hogwarts.",
    "The trio often uncovered mysteries that the teachers were unaware of.",
    "Harry learned about bravery, loyalty, and the power of friendship during his time at school.",
    "In the end, Harry confronted Voldemort and helped bring peace to the wizarding world."
]

embeddings = HuggingFaceEmbeddings(model='all-MiniLM-L6-v2')
text  = 'Who were friends of Harry potter'

embed_doc = embeddings.embed_documents(docc)
embed_docs = np.array(embed_doc)
embed_query = embeddings.embed_query(text)
embed_query = np.array([embed_query])
similarity = cs.cosine_similarity(embed_docs,embed_query)

index=np.argmax(similarity)
print(docc[index])
