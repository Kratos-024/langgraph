from typing import TypedDict

class Person(TypedDict):
    name:str
    age:int

person : Person = {'name':"Adam", 'age':10}, # pyright: ignore[reportAssignmentType]
print(person)