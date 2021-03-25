from flask import Flask, jsonify, request
from marshmallow import Schema, fields
from marshmallow import validate, ValidationError


class LoginValidators(Schema):
    email = fields.Str(required=True, validate=validate.Email())

    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))

#RESGISTER
class CreateRegisterSchema(Schema):

    """name = fixStringClient(content.get("name"))
    lastname = fixStringClient(content.get("lastname"))
    email = fixStringClient(content.get("email"))
    position = fixStringClient(content.get("position"))
    password = fixStringClient(content.get("password"))"""
    
    name = fields.Str(required=True, validate=validate.Length(min=1, max=60))

    lastname = fields.Str(required=True, validate=validate.Length(min=1, max=60))

    email = fields.Str(required=True, validate=validate.Email())

    position = fields.Str(required=True, validate=validate.Length(min=1, max=60))

    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    
#REGISTER PRODUCTS
class RegisterProducts(Schema):
    
    cantidad_producto = fields.Int(required=True, validate=validate.Range(min=1, max=30))

    descripcion_producto = fields.Str(required=True, validate=validate.Length(min=1, max=500))

    img_producto = fields.Str(required=True, validate=validate.Length(min=1, max=500))

    nombre_producto = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    precio_producto = fields.Int(required=True, validate=validate.Range(min=1, max=9000000))

"""cantidad_producto = fixStringClient(json_req['cantidad_producto'])
descripcion_producto = fixStringClient(json_req['descripcion_producto'])
img_producto = json_req['img_producto']
nombre_producto = fixStringClient(json_req['nombre_producto'])
precio_producto = fixStringClient(json_req['precio_producto'])"""

#SearchProductsControllers
class SearchProducts(Schema):
    key_search  = fields.Str(required=True, validate=validate.Length(min=1, max=500))

#SearchUsersChatControllers
class SearchUsersChat(Schema):
    key_search = fields.Str(required=True, validate=validate.Length(min=1, max=500))

#ManageProductsControllers
class ManageProducts(Schema):

    #METODO PUT
    """cantidad_producto = fixStringClient(json_req['cantidad_producto'])
    descripcion_producto = fixStringClient(json_req['descripcion_producto'])
    img_changed = fixStringClient(json_req['img_changed'])
    img_producto = json_req['img_producto']
    img_prev = fixStringClient(img_producto[0])
    img_new = fixBase64String(img_producto[1][23::])
    id_producto = fixStringClient(json_req['id_producto'])
    nombre_producto = fixStringClient(json_req['nombre_producto'])
    precio_producto = fixStringClient(json_req['precio_producto'])"""

    cantidad_producto = fields.Int(required=True, validate=validate.Range(min=1, max=30))
    descripcion_producto = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    img_changed = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    img_producto = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    img_prev = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    id_producto = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    nombre_producto = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    precio_producto = fields.Int(required=True, validate=validate.Range(min=1, max=9000000))

#DeleteFromMyProductsControllers
class DeleteFromMyProducts(Schema):
     reqForFix = fields.Str(required=True, validate=validate.Length(min=1, max=500))
