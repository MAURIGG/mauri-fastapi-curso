###ESTE FICHERO GESTIONA LA CONEXION A MONGODB###

#Base de Datos Local
# from pymongo import MongoClient
# cliente_db = MongoClient().local

from pymongo import MongoClient

cliente_db = MongoClient("mongodb+srv://Mauricio_GaGo_DB:MaJa0419_2004@mauriciog.l5gof3b.mongodb.net/?appName=MauricioG").test