from flask.views import MethodView
from flask import jsonify, request
import bcrypt
import time
import datetime
from services import fixStringClient, checkJwt, dataTableMysql, cryptStringBcrypt, decryptStringBcrypt, encoded_jwt, getBigRandomString,getMinRandomString, cryptBase64, decryptBase64, decode_jwt, initChat,createStringRandom, saveImg
import mysql.connector

class LoginUserControllers(MethodView):
    """
        Login
    """
    def post(self):
        content = request.get_json(force=True)
        email = fixStringClient(content.get("email"))
        password = fixStringClient(content.get("password"))
        dataDB = dataTableMysql("SELECT nombres, apellidos, correo, cargo, clave, id_provisional, llave_privada FROM usuarios WHERE correo = '{}'".format(email))
        

        if len(dataDB) >= 1:
            for data in dataDB:
                if bcrypt.checkpw(bytes(str(password), encoding= 'utf-8'), bytes(str(data[4]), encoding= 'utf-8')):
                    jwt = encoded_jwt(data[5])
                    return jsonify({"logueado": True, "token": jwt, "name": data[0], "lastname": data[1], "email": data[2], "position": data[3], "private_key": data[6]}), 200
                else:
                    return jsonify({"logueado": False, "token": False}), 200
        else:
            return jsonify({"logueado": False, "token": False}), 200

class RegisterUserControllers(MethodView):
    def post(self):
            content = request.get_json()
            name = fixStringClient(content.get("name"))
            lastname = fixStringClient(content.get("lastname"))
            email = fixStringClient(content.get("email"))
            position = fixStringClient(content.get("position"))
            password = fixStringClient(content.get("password"))
            hash_password = cryptStringBcrypt(password)
            _randomID = getBigRandomString()
            _randomStr = createStringRandom(13)
            private_key = str(_randomID) + str(_randomStr)

            data = dataTableMysql("INSERT INTO usuarios(nombres, apellidos, correo, cargo, clave, id_provisional, llave_privada) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, lastname, email, position, hash_password, _randomID, private_key), "rowcount")

            if data:
                time.sleep(1)
                return jsonify({"registered": data}), 200
            else:
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
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

            checkToken = checkJwt(token)
            if not checkToken:
                print("TOKEN NO VALIDO")
                print(token)
                return jsonify({
                "auth_token": False
            }), 200

            json_req = request.get_json(force=True)
            cantidad_producto = fixStringClient(json_req['cantidad_producto'])
            descripcion_producto = fixStringClient(json_req['descripcion_producto'])
            img_producto = json_req['img_producto']
            nombre_producto = fixStringClient(json_req['nombre_producto'])
            precio_producto = fixStringClient(json_req['precio_producto'])

            resultSaveImg = saveImg(img_producto[23::], 'static/img/products/')

            if resultSaveImg[0]:
                res_jwt = decode_jwt(token)
                dataRes = dataTableMysql("INSERT INTO productos(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, creador_producto, imagen_producto) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, res_jwt.get("user_id"), resultSaveImg[1]), "rowcount")

                return jsonify({"saved": dataRes, "auth_token": True}), 200
            else:
                return jsonify({
                "saved": resultSaveImg[0],
                "auth_token": True
            }), 200

        else:
            return jsonify({
                "auth_token": False
            }), 200

class SearchUsersChatControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

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
                    "auth_token": checkToken,
                    "user_id": "Not found data"
                })
                return jsonify(json_res), 200

            id_buscador = decode_jwt(token).get("user_id")

            myresult = dataTableMysql("SELECT nombres, apellidos, correo, cargo, id_provisional FROM usuarios WHERE (nombres LIKE '%{}%' OR apellidos LIKE '%{}%') and id_provisional != '{}'".format(key_search, key_search.lower(), id_buscador))
            
            for data in myresult:
                json_res.append({
                    "nombres": data[0],
                    "apellidos": data[1],
                    "correo": data[2],
                    "cargo": data[3],
                    "found": True,
                    "auth_token": checkToken,
                    "key_search": key_search,
                    "user_id": data[4]
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
                    "auth_token": checkToken,
                    "user_id": "Not found data"
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
            
            checkToken = checkJwt(token[1])
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

class AssignKeyChatInit(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            DataJson = request.get_json(force=True)
            id_provisional_emisor = DataJson["id_emisor"]
            id_provisional_receptor = DataJson["id_receptor"]
            token = tokenR[1]
            
            checkToken = checkJwt(token)
            if not checkToken:
                return jsonify({
                "auth_token": False
            }), 200

            dataJwt = decode_jwt(token)
            if dataJwt.get("user_id") == id_provisional_emisor:
                initInfo = initChat(id_provisional_receptor, id_provisional_emisor)
                return jsonify(initInfo), 200
            else:
                return jsonify({"auth_token": False}), 200
        else:
            return jsonify({"auth_token": False}), 200

