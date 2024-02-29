from pydantic import BaseModel, UUID4

class Cargo(BaseModel):
    name_cargo: str
    id_superior: str

class Funcionario(BaseModel):
    salario: float
    is_true: bool
    cargo: Cargo

class User(BaseModel):
    username: str
    password: str
    funcionario: Funcionario
