def usuario_esquema(usuario)-> dict :
    return {"id":str(usuario["_id"]),
            "usuario":usuario["usuario"],
            "email":usuario["email"]}


def usuarios_esquema(usuarios) -> list:
    return [usuario_esquema(usuario) for usuario in usuarios] 