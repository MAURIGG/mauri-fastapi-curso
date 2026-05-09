from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext #para definir contexto de encriptacion
from datetime import datetime, timedelta #calculo de fechas


ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 1
#un hexadecimal 32 digitos generados en la terminal (aleatorio)
SECRET = "e59300531764c680f4f59163c055257d94f83a06d9eb35b19ff9f4f81739556b"


#Autenticacion
router = APIRouter(prefix="/jwtauth",
                   tags=["JWTAUTH"], 
                   responses= {status.HTTP_404_NOT_FOUND: {"MENSAJE": "USUARIO NO ENCONTRADO"}})


oauth2 = OAuth2PasswordBearer(tokenUrl= "login")


#CONTEXTO DE INCRIPTACION
crypt = CryptContext (schemes= ["bcrypt"])

class Usuario(BaseModel):
    usuario:str
    nombre_completo: str
    email: str
    activo: bool

class UsuarioDB (Usuario):
    contraseña: str

usuarios_db= {
    "maurigg": {
        "usuario":"maurigg",
        "nombre_completo": "Mauricio Galarza",
        "email": "maurig@gmail.com",
        "activo": True,
        "contraseña": "$2b$12$VnJskSE6FPauAqzXyHGXSOyj2R3QzCDBkP9vdtOljJAbb.StMUR6q"
    },
    "mouredev": {
        "usuario":"mouredev",
        "nombre_completo": "Brais Moure ",
        "email": "braismoure@mourede.com",
        "activo": False,
        "contraseña": "$2b$12$ppzM/lUWfrvof9JlXfPT0Of02ghFvrLuD2AcFB86TTSiYBwIwsbhG"
    }
}
def  buscar_usuario_DB (usuario:str):

    if usuario in usuarios_db:
        return UsuarioDB(**usuarios_db[usuario])
    
def  buscar_usuario (usuario:str):

    if usuario in usuarios_db:
        return Usuario(**usuarios_db[usuario])
    

async def auth_usuario(token: str = Depends(oauth2)):
    
    excepcion =HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="CREDENCIALES DE AUTENTICACIÓN INVALIDAS",
                            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        usuario = jwt.decode(token, SECRET, algorithms= ALGORITMO).get("sub")
        if usuario is None:
            raise excepcion
        

    except JWTError: 
        raise excepcion
    return buscar_usuario(usuario)

#verificacion del token 
async def current_user(usuario: Usuario =Depends(auth_usuario)):

    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="USUARIO INACTIVO")
    
    return usuario


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm =Depends()):
    usuario_db = usuarios_db.get(form.username)
    if not usuario_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                            detail="El usuario no es correcto")
    
    usuario = buscar_usuario_DB(form.username)

    if not  crypt.verify(form.password, usuario.contraseña): 
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="Credenciales de autenticación inválidas",
                            headers= {"WWW-Authenticate": "Bearer"})
    #duracion del token
  


    
    access_token = {"sub": usuario.usuario,
                    "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION)}
    #encriptar el token con jwt
    return {"access_token": jwt.encode(access_token,  SECRET,algorithm= ALGORITMO), "token_type": "bearer"}
    

@router.get("/usuarios/me")
async def me(usuario: Usuario = Depends(current_user)):
    return usuario
