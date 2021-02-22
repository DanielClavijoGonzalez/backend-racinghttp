from flask.views import MethodView
from flask import jsonify, request
import time
from config import KEY_TOKEN_AUTH
import datetime
from services import fixStringClient, checkJwt, dataTableMysql, cryptStringBcrypt, decryptStringBcrypt, encoded_jwt
import mysql.connector

class LoginUserControllers(MethodView):
    """
        Example Login
    """
    def post(self):
        #SIMULACION DE LOGIN
        time.sleep(3)
        content = request.get_json()
        correo = fixStringClient(content.get("email"))
        password = fixStringClient(content.get("password"))
        jwt = encoded_jwt(correo)

        if(correo == "grupojed@gmail.com" and password == "JED"):
            return jsonify({"logueado": True, "token": jwt}), 200
        else:
            return jsonify({"logueado": False}), 200

class RegisterUserControllers(MethodView):
    def post(self):
        #time.sleep(3)
            content = request.get_json()
            name = fixStringClient(content.get("name"))
            lastname = fixStringClient(content.get("lastname"))
            email = fixStringClient(content.get("email"))
            position = fixStringClient(content.get("position"))
            password = fixStringClient(content.get("password"))
            hash_password = cryptStringBcrypt(password)

            #decrypted = decryptStringBcrypt(password, hash_password)

            data = dataTableMysql("INSERT INTO usuarios(nombres, apellidos, correo, cargo, clave) VALUES('{}', '{}', '{}', '{}', '{}')".format(name, lastname, email, position, hash_password), "rowcount")
            
            return jsonify({"registered": data}), 200

class SearchProductsControllers(MethodView):
    def post(self):
        #simulacion de espera en el back con 1.5 segundos
        time.sleep(1)
        content = request.get_json()
        busqueda = content.get("search")
        nombre_producto = ["Aceite 125", "Cascos", "Tornillos", "Aceite 150"]
        cantidad_producto = [40, 38, 41, 20000]
        precio_producto = [100, 200000, 400, 23000]
        return jsonify({"nombre_productos": nombre_producto, "cantidad_productos": cantidad_producto,"precio_productos": precio_producto, "search": busqueda}), 200

class AddProductControllers(MethodView):
    def post(self):
        """
            Example for save product
        """
        time.sleep(1)
        content = request.get_json()
        nombre = content.get("nombre")
        referencia = content.get("referencia")
        precio = content.get("precio")
        cantidad = content.get("cantidad")
        return jsonify({"guardado": True}), 200

class SearchUsersChatControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            
            checkToken = checkJwt(token)
            if not checkToken:
                print("TOKEN NO VALIDO")
                print(token)
                return jsonify({
                "auth_token": False
            }), 200

            json_res = []
            json_req = request.get_json(force=True)
            key_search = fixStringClient(json_req["search_key"])
            if len(key_search) == 0:
                json_res.append({
                    "id": -1,
                    "nombres": "Not found data",
                    "apellidos": "Not found data",
                    "correo": "Not found data",
                    "cargo": "Not found data",
                    "clave": "Not found data",
                    "found": False,
                    "key_search": key_search,
                    "auth_token": checkToken
                })
                return jsonify(json_res), 200

            myresult = dataTableMysql("SELECT nombres, apellidos, correo, cargo FROM usuarios WHERE nombres LIKE '%{}%' OR apellidos LIKE '%{}%'".format(key_search, key_search))
            
            for data in myresult:
                json_res.append({
                    "nombres": data[0],
                    "apellidos": data[1],
                    "correo": data[2],
                    "cargo": data[3],
                    "found": True,
                    "auth_token": checkToken,
                    "key_search": key_search
                })
            if len(json_res) == 0:
                json_res.append({
                    "id": -1,
                    "nombres": "Not found data",
                    "apellidos": "Not found data",
                    "correo": "Not found data",
                    "cargo": "Not found data",
                    "clave": "Not found data",
                    "found": False,
                    "key_search": key_search,
                    "auth_token": checkToken
                })
            return jsonify(json_res), 200
        else:
            print("TOKEN NO RECIBIDO")
            return jsonify({
                "auth_token": False
            }), 200

class ValidateJwtControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            
            checkToken = checkJwt(token)
            if checkToken:
                return jsonify({
                "auth_token": checkToken
            }), 200
            else:
                return jsonify({
                "auth_token": checkToken
            }), 200
        else:
            return jsonify({
                "auth_token": False
            }), 200