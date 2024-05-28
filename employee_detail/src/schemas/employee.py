from pydantic import BaseModel


class EmployeeAll(BaseModel):
    emp_name:str
    email:str
    mobile_no:str
    position:str
    password:str

class Emppassword(BaseModel):
    password:str


    

    