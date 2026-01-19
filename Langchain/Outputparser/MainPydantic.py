from pydantic import BaseModel
from typing import List , Optional ,Annotated

class Student(BaseModel):
    name : str = 'nitish'
    age :Annotated[ List[int],"Please insert age"]

new_student  = {'name':['student']}
new_student1  = {'anme':"sintr",'age':[10]}

student = Student(**new_student1)

print(student)
