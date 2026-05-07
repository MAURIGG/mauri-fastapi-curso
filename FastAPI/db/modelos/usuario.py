from pydantic import BaseModel
class Usuario (BaseModel):
    id: str | None = None
    usuario: str
    email: str
