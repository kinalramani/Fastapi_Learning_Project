from fastapi import FastAPI,HTTPException,APIRouter,Depends,Header
from src.models.employee import Employee
from src.schemas.employee import EmployeeAll,Emppassword
from database.database import sessionLocal
from passlib.context import CryptContext
import uuid
from src.utils.token import get_token,decode_token_employee_id,logging_token,decode_token_employee_name,decode_token_employee_password



pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

employee=APIRouter()

db=sessionLocal()


#************************************ register_employee*******************************

@employee.post("/register_employee/",response_model=EmployeeAll)
def create_employee_details(emp:EmployeeAll):
    new_employee=Employee(
        emp_name=emp.emp_name,
        email=emp.email,
        mobile_no=emp.mobile_no,
        position=emp.position,
        password=pwd_context.hash(emp.password),

    )
    db.add(new_employee)
    db.commit()
    return new_employee


#************************************ get employee_details *******************************

@employee.get("/get_employee_detail/{emp_id}",response_model=EmployeeAll)
def get_employee_detail(emp_id:str):
    db_emp=db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail= "employee not found")
    return db_emp


#************************************ get employee_all_details*******************************

@employee.get("/get_employee_all_details/",response_model=list[EmployeeAll])
def get_employee_all_details():
    db_emp=db.query(Employee).filter(Employee.is_active == True).all()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    return db_emp




#************************************ update employee_details_by_token*******************************

@employee.put("/update_employee_details_with_depends/")
def update_employee_details_by_token(emp:EmployeeAll,emp_id=Depends(decode_token_employee_id)):
    db_emp=db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    db_emp.emp_name=emp.emp_name,
    db_emp.email=emp.email,
    db_emp.mobile_no=emp.mobile_no,
    db_emp.position=emp.position,
    db_emp.password=pwd_context.hash(emp.password)


    db.commit()
    db.refresh(db_emp)
    return {"msg":"your detail changed succesfully"}





@employee.put("/update_employee_details_with_header/")
def update_employee_details_by_token(emp:EmployeeAll,emp_id=Header(...)):
    db_emp=db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    db_emp.emp_name=emp.emp_name,
    db_emp.email=emp.email,
    db_emp.mobile_no=emp.mobile_no,
    db_emp.position=emp.position,
    db_emp.password=pwd_context.hash(emp.password)


    db.commit()
    db.refresh(db_emp)
    return {"msg":"your detail changed succesfully"}


#************************************ delete employee_all_by_token_details*******************************

@employee.delete("/delete_employee_with_depends/")
def delete_employee_all_details_by_token(emp_id=Depends(decode_token_employee_id)):
    db_emp=db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    db_emp.is_active=False
    db_emp.is_deleted=True

    db.commit()
    return {"msg":"employee deleted successfully"}






@employee.delete("/delete_employee_all_details_with_header/")
def delete_employee_all_details_by_token(emp_id=Header(...)):
    db_emp=db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    db_emp.is_active=False
    db_emp.is_deleted=True

    db.commit()
    return {"msg":"employee deleted successfully"}

#************************************ toggle employee_details*******************************

@employee.put("/reregister_with_depends")
def toggel_emp(emp:Emppassword,emp_id=Depends(decode_token_employee_id)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    
    if db_emp.is_deleted is True and db_emp.is_active is False:
        if pwd_context.verify(emp.password,db_emp.password):
           
            db_emp.is_deleted = False
            db_emp.is_active = True
            
            db.commit()
            return True
    raise HTTPException(status_code=404,detail= "invalid crediantial")




@employee.put("/reregister_with_header")
def toggel_emp(emp:Emppassword,emp_id=Header(...)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="employee not found")
    
    if db_emp.is_deleted is True and db_emp.is_active is False:
        if pwd_context.verify(emp.password,db_emp.password):
           
            db_emp.is_deleted = False
            db_emp.is_active = True
            
            db.commit()
            return True
    raise HTTPException(status_code=404,detail= "invalid crediantial")


#************************************ forget employee_password_by_token*******************************

@employee.put("/forget_Password_with_depends")

def forget_password_token(user_newpassword : str,emp_id=Depends(decode_token_employee_id)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    if db_emp is  None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(user_newpassword)
    

    db.commit()
    return "Forget Password successfully"




@employee.put("/forget_Password_with_header")

def forget_password_token(user_newpassword : str,emp_id=Header(...)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    if db_emp is  None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(user_newpassword)
    

    db.commit()
    return "Forget Password successfully"




#************************************ reset_password_by_token*******************************

@employee.put("/reset_password_with_depends")
def reset_password_token(oldpassword:str,newpassword:str,emp_id=Depends(decode_token_employee_id)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpassword,db_emp.password):
        db_emp.password = pwd_context.hash(newpassword)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}
    



@employee.put("/reset_password_with_header")
def reset_password_token(oldpassword:str,newpassword:str,emp_id=Header(...)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpassword,db_emp.password):
        db_emp.password = pwd_context.hash(newpassword)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}
    


#************************************encode_logging *******************************

@employee.get("/encode_logging")
def token_logging(emp_name:str,password:str):
    access_token = logging_token(emp_name,password)
    return access_token


#************************************logging *******************************

@employee.get("/logging_with_depends")
def logging(emp_name = Depends(decode_token_employee_name),password = Depends(decode_token_employee_password)):
    # emp_name = decode_token_employee_name(token)
    # password = decode_token_employee_password(token)
    db_emp = db.query(Employee).filter(Employee.emp_name==emp_name,Employee.is_active ==True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    return "loging successfully"



@employee.get("/logging_with_header")
def logging(emp_name = Header(...),password = Header(...)):
    # emp_name = decode_token_employee_name(token)
    # password = decode_token_employee_password(token)
    db_emp = db.query(Employee).filter(Employee.emp_name==emp_name,Employee.is_active ==True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    return "loging successfully"





@employee.put("/reset_password_with_header")
def reset_password_token(oldpassword:str,newpassword:str,emp_id=Header(...)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpassword,db_emp.password):
        db_emp.password = pwd_context.hash(newpassword)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}


#************************************encode token*******************************
@employee.get("/encode_token")
def encode_details(id:str):
    access_token = get_token(id)
    return access_token



#************************************ decode token*******************************

#decode id
@employee.get("/decode_id")
def decode_id(token:str):
    employee_id = decode_token_employee_id(token)
    return employee_id





#---------------------------------- depends demo with postman -----------------------------


def sum(a:int,b:int):
    return a+b



@employee.get("/sum_of_two_number")
def sum_of_two_number(sum=Depends(sum)):
    new_sum = sum
    return new_sum
    