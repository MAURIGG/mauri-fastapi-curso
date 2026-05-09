from fastapi import APIRouter,HTTPException,status, Depends #Depends: para gestion de usuario y contra
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#OAuth2PasswordBearer: clase de gestionar usuario y contraseña
#OAuth2PasswordRequestForm: forma de que se envia a la api (usuario y contraseña)
# y la forma en que el backend captura para ver si es usuario del sistema 

router = APIRouter(prefix="/basicauth",
                   tags=["BASICAUTH"], 
                   responses= {status.HTTP_404_NOT_FOUND: {"MENSAJE": "USUARIO NO ENCONTRADO"}})


oauth2= OAuth2PasswordBearer(tokenUrl="login")

#Entidad usuario
class Usuario(BaseModel):
    usuario: str
    nombre_completo: str
    email: str
    activo: bool


class UsuarioDB(Usuario): #la clase hereda de la clase Usuario
    contraseña:str #Aparte de lo heredado se le agrega uno más

usuarios_db = {
    "maurigg": {
        "usuario":"maurigg",
        "nombre_completo": "Mauricio Galarza",
        "email": "maurig@gmail.com",
        "activo": True,
        "contraseña": "123456" #debe estar encriptada
    },
    "mouredev": {
        "usuario":"mouredev",
        "nombre_completo": "Brais Moure ",
        "email": "braismoure@mourede.com",
        "activo": False,
        "contraseña": "654321" #debe estar encriptada
    }
}


#Mecanismo para ver si el usuario está en la base de datos
def  buscar_usuario_DB (usuario:str):

    if usuario in usuarios_db:
        return UsuarioDB(**usuarios_db[usuario])
    
def  buscar_usuario (usuario:str):

    if usuario in usuarios_db:
        return Usuario(**usuarios_db[usuario])
    
#criterios de dependencias
async def current_user(token: str =Depends(oauth2)):
    usuario = buscar_usuario(token)
    if not usuario:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="CREDENCIALES DE AUTENTICACIÓN INVALIDAS",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="USUARIO INACTIVO")
    
    return usuario
    

#gestionar usuarios
@router.post("/login") #enviar usuario y contra
async def login(form: OAuth2PasswordRequestForm = Depends()): #capturar usuario y contraseña
   
   #BUSCAR EL USUARIO DENTRO DE LA BASE DE DATOS
    usuario_db = usuarios_db.get(form.username)
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "EL USUARIO NO ES CORRECTO")
    
    #SI ENCUENTRA EL USUARIO OBTENGO SUS DATOS 
    usuario = buscar_usuario_DB(form.username)

    #verifico si la contra son iguales
    if not form.password == usuario.contraseña:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "LA CONTRASEÑA NO ES CORRECTA")

    #SI TENEMOS EL USUARIO: retornamos un access_token y de que tipo es el token (ES BEARER)
   
    #el access_token sirve para que no tenga que ingresar cada vez que solicito algun dato 
    #el usuario y a contraseña y  solo ingreso el token que me dá
    return {"access_token": usuario.usuario, "token_type": "bearer"}


#Mostrar una vez autenticado cual es el usuario
@router.get("/usuarios/me")

async def me(usuario: Usuario = Depends(current_user)): 
     return usuario 