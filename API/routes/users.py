from API.classes.user import User
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
import jwt
from jwt import PyJWTError
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

fakedb = []

@app.post("/register")
async def register(createUser: User, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/autentication"))):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        username_exists = any(user['username'] == createUser.username for user in fakedb)
        if username_exists:
            return({"message":"Nome já existente."})
        else:
            fakedb.append({
                "id":str(uuid4()),
                "username":createUser.username,
                "password":createUser.password,
                "funcionario":{
                    "is_true":createUser.funcionario.is_true,
                    "salario":createUser.funcionario.salario,
                    "cargo":{
                        "name_cargo":createUser.funcionario.cargo.name_cargo,
                        "id_superior":createUser.funcionario.cargo.id_superior
                    }
                }})
            print(fakedb)
            return({"message":"usuario cadastrado com sucesso"})
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")