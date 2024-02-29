from API.classes.user import User
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from uuid import uuid4
import jwt
from jwt import PyJWTError
import datetime
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def inicio():
    return """
    <html>
        <head>
            <title> Inicio </title>
        </head>
        <body>
            <h1> Tela de incio </h1>
        </body>
    </html>
    """

fakedb = [{'id':'123456','username':'lucascvlh','password':'123456'}]
# Função para autenticar usuário (apenas para fins de demonstração)
def authenticate_user(username: str, password: str):
    for dataUser in fakedb:
        if dataUser['username'] != username or dataUser['password'] != password:
            return None
        return dataUser

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

# Rota de login para obter um token JWT
@app.post("/autentication")
async def login(user: User):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Rota protegida que requer um token JWT para acessar
@app.get("/home")
async def home(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/autentication"))):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        #Aqui aonde vai continuar o código depois que entrar na rota
        #...
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return {"message": "You are authenticated!"}

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