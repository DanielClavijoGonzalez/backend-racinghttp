
from flask.views import MethodView
from flask import jsonify, request
import time



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
        if(correo == correv and password == passwordv):
            return jsonify({"Datos ingresado correctamente": True}), 200
        else:
            return jsonify({"Datos ingresado incorrectamente": True}), 200

class RegisterUserControllers(MethodView):
    def post(self):
        #simulacion de espera en el back con 1.5 segundos
        time.sleep(3)
        content = request.get_json()
        nombres = content.get("nombres")
        documento = content.get("documento")
        correo = content.get("correo")
        password = content.get("password")
        return jsonify({"Usuario registrado": True, "nombre": nombres,"documento":documento,"correo":correo,"password":password}), 200
