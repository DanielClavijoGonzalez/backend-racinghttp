import os
from flask.views import MethodView
from flask import jsonify, request
import bcrypt
import time
import datetime
from services import fixStringClient, checkJwt, dataTableMysql, cryptStringBcrypt, decryptStringBcrypt, encoded_jwt, getBigRandomString,getMinRandomString, cryptBase64, decryptBase64, decode_jwt, initChat,createStringRandom, fixBase64String, saveFileCloudDpBx, fixImgB64
from services import updateFileCloudDpBx
import mysql.connector
from validators import LoginValidators, CreateRegisterSchema

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
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

            checkToken = checkJwt(token)
            if not checkToken:
                print("TOKEN NO VALIDO")
                print(token)
                return jsonify({"auth_token": False}), 200

            json_res = []
            json_req = request.get_json(force=True)
            key_search = fixStringClient(json_req["search_key"])
            if len(key_search) == 0:
                json_res.append({"found": False,"key_search": key_search,"auth_token": checkToken})
                return jsonify(json_res), 200

            id_buscador = decode_jwt(token).get("user_id")

            myresult = dataTableMysql("SELECT p.nombre_producto, p.cantidad_producto, p.precio_producto, p.descripcion_producto, p.imagen_producto, p.creador_producto, p.id, concat(u.nombres, ' ', u.apellidos, ' ', u.cargo) as usuario_creador FROM productos p, usuarios u WHERE p.creador_producto=u.id_provisional AND nombre_producto LIKE '%{}%' AND creador_producto != '{}' AND estado_producto != 0".format(key_search.lower(), id_buscador))

            for data in myresult:
                json_res.append({
                    "nombre_producto": data[0],
                    "cantidad_producto": data[1],
                    "precio_producto": data[2],
                    "descripcion_producto": data[3],
                    "imagen_producto": data[4],
                    "creador_producto": data[5],
                    "id_producto": data[6],
                    "usuario_creador": data[7],
                    "found": True,
                    "auth_token": checkToken,
                    "key_search": key_search
                })

            if len(json_res) == 0:
                json_res.append({"found": False,"key_search": key_search,"auth_token": checkToken})

            return jsonify(json_res), 200
        return jsonify({"auth_token": False}), 200

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

            imgFixed = fixImgB64(img_producto)

            resultSaveImg = saveFileCloudDpBx(route='/products/', img=imgFixed[1])

            if resultSaveImg[0]:
                res_jwt = decode_jwt(token)
                dataRes = dataTableMysql("INSERT INTO productos(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, creador_producto, imagen_producto) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, res_jwt.get("user_id"), resultSaveImg[1]), "rowcount")

                return jsonify({"saved": dataRes, "auth_token": True}), 200
            else:
                return jsonify({
                "saved": False,
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
        time.sleep(3)
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

class AssignKeyChatInitControllers(MethodView):
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

class ManageProductsControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

            checkToken = checkJwt(token)

            if not checkToken:
                return jsonify({"auth_token": False}), 200

            jwt_data = decode_jwt(token)
            my_products = 0
            my_products_buy = 0
            my_register_products = []
            dataSqlReg = dataTableMysql("SELECT r.fecha_compra, p.precio_producto, u.nombres AS nombre_comprador, u.apellidos AS apellidos_comprador, u.foto_perfil AS foto_perfil_comprador, r.volumen_adquirido, u.id_provisional AS id_comprador FROM registro_compra r, usuarios u, productos p WHERE r.producto_adquirido = p.id AND u.id_provisional = r.comprador AND (r.fecha_compra >= DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY) AND r.fecha_compra <= DATE_ADD(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 6 DAY ) ) AND r.vendedor = '{}'".format(jwt_data.get("user_id")))
            dataSqlMyProd = dataTableMysql("SELECT count(*) AS productos_actuales FROM productos WHERE creador_producto = '{}' and estado_producto != 0".format(jwt_data.get("user_id")))
            dataSqlProdBuy = dataTableMysql("SELECT sum(volumen_adquirido) AS productos_adquiridos FROM registro_compra WHERE comprador = '{}'".format(jwt_data.get("user_id")))

            for col in dataSqlReg:
                my_register_products.append({
                    "date": col[0],
                    "price_product": col[1],
                    "name_buyer": col[2],
                    "lastname_buyer": col[3],
                    "profile_image_buyer": col[4],
                    "units_purchased": col[5],
                    "id_buyer": col[6]
                })

            for col in dataSqlMyProd:
                my_products = col[0]

            for col in dataSqlProdBuy:
                if col[0] == None:
                    my_products_buy = 0
                else:
                    my_products_buy = col[0]

            print(type(my_products_buy))
            print(my_products_buy)
            return jsonify({
                "auth_token": True,
                "my_products": str(my_products),
                "my_purchased_products": str(my_products_buy),
                "my_register_products": my_register_products
            }), 200
        else:
            return jsonify({"auth_token": False}), 200

    def put(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

            checkToken = checkJwt(token)

            if not checkToken:
                return jsonify({"auth_token": False}), 200

            jwt_data = decode_jwt(token)
            jsonResponse = []

            json_req = request.get_json(force=True)
            cantidad_producto = fixStringClient(json_req['cantidad_producto'])
            descripcion_producto = fixStringClient(json_req['descripcion_producto'])
            img_changed = fixStringClient(json_req['img_changed'])
            img_producto = json_req['img_producto']
            img_prev = fixStringClient(img_producto[0][-27::][:22])
            img_new_fix = fixBase64String(img_producto[1])
            img_new = fixImgB64(img_new_fix)

            id_producto = fixStringClient(json_req['id_producto'])
            nombre_producto = fixStringClient(json_req['nombre_producto'])
            precio_producto = fixStringClient(json_req['precio_producto'])

            if img_changed == True:
                resultSaveImg = updateFileCloudDpBx(route='/Products/', img=img_new, imgPrev=img_prev)
                # deletePrevImg = delFile(img_prev, '../frontend-racinghttp/src/assets/img/products/')
                if resultSaveImg[0]:
                    dataSql = dataTableMysql("UPDATE productos SET nombre_producto = '{}', cantidad_producto = '{}', precio_producto = '{}', descripcion_producto = '{}', imagen_producto = '{}' WHERE id = '{}' and creador_producto = '{}'".format(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, resultSaveImg[1], id_producto, jwt_data.get("user_id")), 'rowcount' )
                    return jsonify({"auth_token": True,"saved": dataSql}), 200
                else:
                    return jsonify({"auth_token": True,"saved": False}), 200
            else:
                dataSql = dataTableMysql("UPDATE productos SET nombre_producto = '{}', cantidad_producto = '{}', precio_producto = '{}', descripcion_producto = '{}' WHERE id = '{}' and creador_producto = '{}'".format(nombre_producto, cantidad_producto, precio_producto, descripcion_producto, id_producto, jwt_data.get("user_id")), 'rowcount' )
                return jsonify({"auth_token": True,"saved": dataSql}), 200

class ManageMyProductsControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]

            checkToken = checkJwt(token)

            if not checkToken:
                return jsonify({"auth_token": False}), 200

            jwt_data = decode_jwt(token)
            jsonResponse = []

            dataSql = dataTableMysql("SELECT id, nombre_producto, cantidad_producto, precio_producto, descripcion_producto, imagen_producto FROM productos WHERE creador_producto = '{}' and estado_producto != 0".format(jwt_data.get("user_id")))

            for col in dataSql:
                jsonResponse.append({
                    "id": col[0],
                    "img_product": col[5],
                    "price_product": col[3],
                    "vol_product": col[2],
                    "name_product": col[1],
                    "description_product": col[4],
                    "check": False,
                    "auth_token": checkToken
                })
            # if len(jsonResponse) == 0:
            #     jsonResponse.append({
            #         "auth_token": checkToken
            #     })

            return jsonify(jsonResponse), 200
        else:
            return jsonify({"auth_token": False}), 200

class DeleteFromMyProductsControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            tokenR = request.headers.get('Authorization').split(" ")
            token = tokenR[1]
            json_req = request.get_json(force=True)
            reqForFix = json_req.get("product_id")
            product_id = []
            for item in reqForFix:
                product_id.append(fixStringClient(item))

            checkToken = checkJwt(token)

            if not checkToken:
                return jsonify({"auth_token": False}), 200

            jwt_data = decode_jwt(token)
            dataSql = False

            for data in product_id:
                print(data)
                dataSql = dataTableMysql("UPDATE productos SET estado_producto = '0' WHERE creador_producto = '{}' and id = '{}'".format(jwt_data.get("user_id"), data), "rowcount")


            return jsonify({"auth_token": True, "deleted": dataSql}), 200
        else:
            return jsonify({"auth_token": False}), 200
