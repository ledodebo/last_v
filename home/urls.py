from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 



urlpatterns = [
    path('', views.index,name="home"),
    path('product/<int:pk>', views.producct,name="products"),
    path('login/', views.login_usr,name="login"),
    path('logout/', views.logout_usr,name="logout"),
    path('register/', views.register_usr,name="reg"),
    path('catagory/', views.catagory,name="cag"),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('product/add/', views.add_to_cart, name='add_to_cart'),
    path('catagory/add/', views.add_to_cart, name='add_to_cart'),
    path('checkout/inc/', views.innc, name='inc'),
    path('cart/mines/', views.remove_iteam, name='remove_cart'),
    path('cart/add/', views.add_iteam, name='add_cart'),
    path('cart/delete/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout,name="check"),
    path('google/', views.google,name="google"),
    path('order_placed_successfully /', views.order_placed,name="done"),
    path('search/<str:pk>', views.search,name="search"),
   path('product/checkrn/<int:pk>', views.checkrn,name="checkrn"),
    path('/getprice/', views.getprice,name="getprice"),
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
