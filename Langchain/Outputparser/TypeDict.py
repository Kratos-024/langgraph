from typing import TypedDict, List , Literal, Annotated

class Person(TypedDict):
    name: Annotated[List[str],'Should be string']
    age:Annotated[int,'Should be int']

person : Person = {'name':["Adam",'fg'], 'age':10}
print(person)
