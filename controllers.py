from flask.views import MethodView
from flask import jsonify, request
import time
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import datetime



class LoginUserControllers(MethodView):
    """
        Example Login
    """
    def post(self):
        #SIMULACION DE LOGIN
        correv="grupojed@gmail.com"
        passwordv="JED"
        time.sleep(3)
        content = request.get_json()
        correo = content.get("correo")
        password = content.get("password")

        encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'email': correo}, KEY_TOKEN_AUTH , algorithm='HS256')

        if(correo == correv and password == passwordv):
            return jsonify({"logueado": True, "token": encoded_jwt}), 200
        else:
            return jsonify({"logueado": False}), 200

class RegisterUserControllers(MethodView):
    def post(self):
        #simulacion de espera en el back con 1.5 segundos
        time.sleep(3)
        content = request.get_json()
        nombres = content.get("nombres")
        documento = content.get("documento")
        correo = content.get("correo")
        password = content.get("password")
        salt = bcrypt.gensalt()

        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)
        
        return jsonify({"usuarioRegistrado": True, "nombre": nombres,"documento":documento,"correo":correo,"password":password}), 200

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