from django.urls import path
from . views import *
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('women/', views.women_category, name="women"),
    path('men/', views.men_category, name="men"),
    path('kids/', views.kids_category, name="kids"),
    path('all_products/', views.all_products, name="all_products"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("register/", UserRegistrationView.as_view(), name="registration"),
    path("logout/", UserLogoutView.as_view(), name="userlogout"),
    path("login/", UserLoginView.as_view(), name="userlogin"),

    path("category/", views.sub_items, name="subitem"),


    path("women/<slug:data>", views.womencateg, name="womencateg"),
    path("men/<slug:data>", views.mencateg, name="mencateg"),
    path("kids/<slug:data>", views.kidcateg, name="kidcateg"),


    path('add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name="addtocart"),
    path('my-cart/', MyCartView.as_view(), name="mycart"),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name="managecart"),
    path('checkout/', views.checkout, name="checkout"),

    path('search/', SearchView.as_view(), name='search')


]