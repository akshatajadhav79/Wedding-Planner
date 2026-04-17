from django.urls import path
from Organizer.views import *

urlpatterns = [
    path('Orgadmin', Orgadmin,name='Orgadmin'),
    
    path('Org_logout/', Org_logout,name='Org_logout'),
    path('org_register/', org_register,name='org_register'),
    path('org_login/', org_login,name='org_login'),
    path('org_profile/', org_profile,name='org_profile'),
    path('organization/', organization,name='organization'),
    path('org_forgetPass/', org_forgetPass,name='org_forgetPass'),
    path('orginfo/<oid>,<cid>',orginfo,name='orginfo'),
    path('whoview/',whoview,name='whoview')
   
]
