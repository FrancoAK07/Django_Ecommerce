from .views import (
    home,
    product_details,
    login_user,
    logout_user,
    register_user,
    update_user,
    update_password,
    update_info,
    search_product,
)
from django.urls import path


urlpatterns = [
    path("", home, name="home"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("update_user/", update_user, name="update_user"),
    path("update_info/", update_info, name="update_info"),
    path("update_password/", update_password, name="update_password"),
    path("search/", search_product, name="search"),
    path("products/<slug:slug>", product_details, name="product_details"),
]
