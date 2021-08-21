from django.urls import path
from . views import ProductDetailView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('women/', views.women, name="women"),
    path('men/', views.men, name="men"),
    path('kids/', views.kids, name="kids"),
    path('cart/', views.cart, name="cart"),
    path('profile/', views.profile, name="profile"),
    path('all_products/', views.all_products, name="all_products"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail")
]