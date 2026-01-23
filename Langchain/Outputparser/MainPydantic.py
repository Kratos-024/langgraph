from pydantic import BaseModel, EmailStr, Field
from typing import List , Optional ,Annotated

class Student(BaseModel):
    name : str = 'nitish'
    age :Annotated[ List[int],"Please insert age"]=Field(gt=0,lt=10, description='DOB')
    cgpa : Annotated[Optional[List[int]],"please enter cgpa"]
    dob : float = Field(gt=0,lt=10, description='DOB')


new_student  = {'name':['student']}
new_student1  = {'anme':"sintr",'age':[10]}
new_student2  = {'name':'dfdd','age':[1],"cgpa":[2],'dob':3}
student = Student(**new_student2)

print(student.model_dump_json())
