from django.urls import path
from Customer.views import *


urlpatterns = [
    path('custadmin', custadmin,name='custadmin'),
    
    path('cust_logout/', cust_logout,name='cust_logout'),
    path('cust_register/', cust_register,name='cust_register'),
    path('cust_login/', cust_login,name='cust_login'),
    path('cust_forgetPass/', cust_forgetPass,name='cust_forgetPass'),
    path('profile', profile,name='profile'),
    path('Wishlist/', Wishlist,name='Wishlist'),

   
]


