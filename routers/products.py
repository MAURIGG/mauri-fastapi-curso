from fastapi import APIRouter

router = APIRouter(prefix= "/productos", 
                   tags= ["productos"], #Para documentacion para agrupar 
                   responses={404:{"MENSAJE": "NO ENCONTRADO"}})

lista_productos = ["Producto 1", "Producto 2", 
             "Producto 3", "Producto 4", "Producto 5"]

#devuelve todos los productos
@router.get("/") #este / ya apunta al prefix de router
async def productos():
    return lista_productos

##devuelve el producto del id que ingreso

@router.get("/{id}")

async def productos(id: int ):
    return lista_productos[id]