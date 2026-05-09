### USUARIOS DB API ###


from fastapi import APIRouter, HTTPException, status
from db.modelos.usuario import Usuario
from db.cliente import cliente_db
from db.schemas.usuario import usuario_esquema, usuarios_esquema
from bson import ObjectId

router = APIRouter(prefix="/usuariodb",
                   tags=["USUARIO_DB"], 
                   responses= {status.HTTP_404_NOT_FOUND: {"MENSAJE": "USUARIO NO ENCONTRADO"}})


#Entidad usuario

   

usuarios_lista = []
#buscar de forma generica, es decir se busca poe  email, nombre o id
def buscar_usuario(field:str, key):
    try:
        usuario= cliente_db.usuarios.find_one({field: key})
        return Usuario(**usuario_esquema(usuario))
    except:
        return {"ERROR:" : " NO SE ENCONTRÓ EL ID INGRESADO."}


#@app.get("/usuarios")
@router.get("/", response_model= list[Usuario])
async def usuarios():
    return usuarios_esquema(cliente_db.usuarios.find())


@router.get("/query") #QUERY
async def usuario(id: str):
   return buscar_usuario("_id", ObjectId(id))


@router.get("/{id}") #PATH
async def usuario_path(id:str):
     return buscar_usuario("_id", ObjectId(id))
    

@router.post("/", response_model= Usuario, status_code= status.HTTP_201_CREATED)
async def usuario(usuario: Usuario): 
      #Verificar si el id del usuario agregado ya existe
    if type(buscar_usuario("email", usuario.email)) == Usuario:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                                          detail= "EL USUARIO YA EXISTE")
    
    
    #para que el usuario sea un json (diccionario)
    #Mongodb solo permite json
    usuario_dict =dict(usuario) 
   
    #elimino el id que ingresa y mongodb genera de forma automatica
    del usuario_dict["id"]

    id = cliente_db.usuarios.insert_one(usuario_dict).inserted_id
    #usuario_esquema: me devuelve de tipo Usuario y no en forma de json
    nuevo_usuario = usuario_esquema(cliente_db.usuarios.find_one({"_id": id }))

    return Usuario(**nuevo_usuario)


#PUT actualizar
@router.put("/", response_model= Usuario)
async def actualizar_usuario(usuario: Usuario):

   
    usuario_dict =dict(usuario) 
    del usuario_dict["id"]

    try:
        cliente_db.usuarios.find_one_and_replace(
            {"_id": ObjectId(usuario.id)}, usuario_dict)
         
    except:
         return{"ERROR":"NO SE HA ACTUALIZADO"}
    
    return buscar_usuario("_id", ObjectId(usuario.id))


#DELETE eliminar usuario
@router.delete("/{id}")
async def usuario (id: str, status_code= status.HTTP_204_NO_CONTENT):

    encontrar = cliente_db.usuarios.find_one_and_delete({"_id": ObjectId(id)})
    
    if not encontrar:
        return {"ERROR": "NO SE HA ELIMINADO EL USUARIO"}
    else:
        return {"FINALIZADO": "EL USUARIO SE HA ELIMINADO"}

