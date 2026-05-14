#importar el modulo fastapi
from fastapi import FastAPI
from routers import products
from routers import users

from routers import basic_auth_users
from routers import jwt_auth_users
from fastapi.staticfiles import StaticFiles #usar mount

from routers import usuario_db
#LLamamos a la clase FastAPI
app = FastAPI()


#ROUTERS 
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(usuario_db.router)

#Mostrar imagen (RECURSOS ESTATICOS)
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/") #raiz de la ip donde está ejecutandose nuestra API
async def root():
    return "Hola FasAPI!"

@app.get("/url")
async def url(): #siempre cada función con nombre distinto
    return {"url":"http://maurigg.com/python"}
