from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os 
from jose import JWTError,jwt



load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))
def get_token(id):
    payload = {
        "employee_id": id,
        "exp": datetime.utcnow() + timedelta(minutes=5),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token



def logging_token(emp_name,password):
    payload = {
        "emp_name" :emp_name,
        "emp_password" : password,
        "exp" : datetime.utcnow() + timedelta(minutes=5)
    }
    access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token




def decode_token_employee_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        employee_id = payload.get("employee_id")
        if not employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return employee_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    



def decode_token_employee_name(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emp_name = payload.get("emp_name")
        if not emp_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="empname not exists in payload",
            )
        return emp_name
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    





def decode_token_employee_password(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emp_password = payload.get("emp_password")
        if not emp_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return emp_password
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )