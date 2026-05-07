### FICHERO USADO PARA EXPLICACION SENCILLA PASO A PASO
### SIN USAR MONGODB ###



#from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#app =FastAPI()
#iniciar el server: uvicorn users:app --reload
#
#
#
router = APIRouter(prefix="/usuarios",
                   tags=["USUARIOS"], 
                   responses= {404: {"MENSAJE": "USUARIO NO ENCONTRADO"}})


#Entidad usuario
class Usuario(BaseModel ):
    id: int
    nombre: str 
    apellido: str
    url: str
    edad: int

usuarios_lista = [Usuario(id=1, nombre="Brais", apellido="Moure", url="https://moure.dev", edad= 38),
                  Usuario(id=2, nombre="Mauri", apellido="Galarza", url="https://mauri.com", edad=22),
                  Usuario(id=3, nombre="Luis", apellido="Morale", url="https://luis.py", edad= 36)]

def buscar_usuario(id:int):
    try:
        #filter me regresa todos los que se cumple con u.id ==id
        return list( filter(lambda u: u.id==id, usuarios_lista))[0]
    except:
        return {"ERROR:" : " NO SE ENCONTRÓ EL ID INGRESADO."}

#@app.get("/usuariosjson")
@router.get("/json")
async def usuariosjson():
    return [{"nombre": "Brais", "apellido": "Moure", "url": "https://moure.dev", "edad":38}, 
            {"nombre":"Mauri", "apellido": "Gomez", "url": "https://mauri.com","edad":22 },
            {"nombre": "Luis", "apellido": "Morales", "url": "https://luis.py", "edad":36}]

#@app.get("/usuarios")
@router.get("/")
async def usuarios():
    #crear de forma manual
    #return Usuario(nombre="Mauri", apellido="Galarza", url="https://mauri.com", edad=22)
    #crear una listra fuera de la función
    return usuarios_lista

#QUERY
#@app.get("/usuarioquery/")
@router.get("/query")
async def usuario(id:int):
   return buscar_usuario(id)

#PATH se usa ccuando es obligatorio (id)
#@app.get("/usuario/{id}")
@router.get("/{id}")
async def usuario(id:int):
    return buscar_usuario(id)
    

#POST crear usuario
#@app.post("/usuario/", response_class= Usuario, status_code= 201)
@router.post("/", response_model= Usuario, status_code= 201)
async def usuario(usuario: Usuario): #parametro usuario del tipo Usuario(clase)
     
     #Verificar si el id del usuario agregado ya existe
    if type(buscar_usuario(usuario.id)) == Usuario:
        #cuando lanzamos un error usamos raise 
        raise HTTPException(status_code=404, detail= "EL USUARIO YA EXISTE")
    else:
        usuarios_lista.append(usuario)
        return usuario

#get leer usuario

#PUT actualizar
#@app.put("/usuario/")
@router.put("/", response_model= Usuario, status_code= 200)
async def user(usuario: Usuario):
    encontrar = False
    for indice, u in enumerate(usuarios_lista):
        if u.id == usuario.id:
            usuarios_lista[indice] = usuario
            encontrar = True
    if not encontrar:
        raise HTTPException(status_code=404, detail="EL USUARIO NO SE HA ACTUALIZADO")
    else:
        return usuario  


#DELETE eliminar usuario
#@app.delete("/usuario/{id}")
@router.delete("/{id}")
async def usuario (id: int):
    encontrar =False
    for indice, u in enumerate(usuarios_lista):
        if u.id == id:
            del usuarios_lista[indice]
            encontrar = True
    
    if not encontrar:
        return {"ERROR": "NO SE HA ELIMINADO EL USUARIO"}
    else:
        return {"FINALIZADO": "EL USUARIO SE HA ELIMINADO"}

