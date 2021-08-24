from django.urls import path
from . views import ProductDetailView, UserRegistrationView, UserLogoutView, UserLoginView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('women/', views.women, name="women"),
    path('men/', views.men, name="men"),
    path('kids/', views.kids, name="kids"),
    path('cart/', views.cart, name="cart"),
    path('all_products/', views.all_products, name="all_products"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("register/", UserRegistrationView.as_view(), name="registration"),
    path("logout/", UserLogoutView.as_view(), name="userlogout"),
    path("login/", UserLoginView.as_view(), name="userlogin"),

    path("category/", views.subitem, name="subitem"),


    path("women/<slug:data>", views.winteritems, name="winteritemsdata"),


    #path("winter/", views.winter, name="winter")

]