from controllers import LoginUserControllers, RegisterUserControllers, SearchProductsControllers, AddProductControllers


user = {
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "register_user": "/api/v01/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api")
}

admin = {
    "search_product_admin": "/api/v01/search/product", "search_products_controllers": SearchProductsControllers.as_view("search_products_api"),
    "add_products_admin": "/api/v01/add/product",
     "add_product_controllers": AddProductControllers.as_view("add_products_api")
}