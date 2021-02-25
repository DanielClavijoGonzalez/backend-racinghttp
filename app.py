from flask import Flask
from routes import *
from flask_cors import CORS
from config import SECRET_KEY, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_DB
from config import MYSQL_PASSWORD

app = Flask(__name__)

CORS(app, resources={
    r"/*": {"origins": "*"},
    r"/*": {
        "origins": ["*"],
        "methods": ["OPTIONS", "POST"],
        "allow_headers": ["Authorization", "Content-Type"],
        }
    })

app.secret_key = SECRET_KEY

app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["register_user"], view_func=user["register_user_controllers"])
app.add_url_rule(admin["search_product_admin"], view_func=admin["search_products_controllers"])
app.add_url_rule(admin["add_products_admin"], view_func=admin["add_product_controllers"])
app.add_url_rule(admin["search_users_admin"], view_func=admin["search_users_controllers"])
app.add_url_rule(user["check_jwt"], view_func=user["check_jwt_controllers"])
app.add_url_rule(admin["asign_init_chat"], view_func=admin["asign_init_chat_controllers"])