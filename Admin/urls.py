from django.urls import path
from Admin.views import *


urlpatterns = [
    path('adminLogin/', adminLogin,name='adminLogin'),
    path('',base,name='base'),
    path('hostadmin',hostadmin,name='hostadmin'),
    path('logout_admin',logout_admin,name='logout_admin'),
    path('service',service,name='service'),
    path('Contact',Contact,name='Contact'),
    path('create_categoty',create_categoty,name='create_categoty'),
    path('bothlogin',bothlogin,name='bothlogin'),
    path('activate_planner',activate_planner,name='activate_planner'),
    path('Toactivate/<int:id>',Toactivate,name='Toactivate'),

]
