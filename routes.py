from controllers import *

user = {
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),

    "register_user": "/api/v01/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),

    "check_jwt": "/api/v01/check/jwt",
    "check_jwt_controllers": ValidateJwtControllers.as_view("check_jwt_api")
}

admin = {
    "search_product_admin": "/api/v01/search/product", "search_products_controllers": SearchProductsControllers.as_view("search_products_api"),

    "add_products_admin": "/api/v01/add/product",
     "add_product_controllers": AddProductControllers.as_view("add_products_api"),
     "search_users_admin": "/api/v01/search/users",
     "search_users_controllers": SearchUsersChatControllers.as_view("search_users_api"),

     "asign_init_chat": "/api/v01/init/chat",
     "asign_init_chat_controllers": AssignKeyChatInitControllers.as_view("asign_init_chat_api"),

     "manage_products": "/api/v01/manage/products",
     "manage_products_controllers": ManageProductsControllers.as_view("manage_products_api"),

     "manage_my_products": "/api/v01/manage/myproducts",
     "manage_my_products_controllers": ManageMyProductsControllers.as_view("manage_my_products_api"),

     "manage_my_products": "/api/v01/manage/myproducts",
     "manage_my_products_controllers": ManageMyProductsControllers.as_view("manage_my_products_api"),

     "delete_from_my_products": "/api/v01/manage/myproducts/delete",
     "delete_from_my_products_controllers": DeleteFromMyProductsControllers.as_view("delete_from_my_products_api"),

    "request_products": "/api/v01/request/products/<int:id>/<int:volume>/",
     "request_products_controllers": RequestProductControllers.as_view("request_products_api"),

     "request_purchased_products": "/api/v01/purchased/products/<string:token>/<string:rol>/",
     "request_purchased_products_controllers": GetPurchasedProducts.as_view("request_purchased_products_api"),
}
