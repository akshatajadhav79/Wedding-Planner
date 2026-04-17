from django.contrib import admin
from .models import role_master,orgnizer_master,category_master,organizer_info_master,customer,whoview_master,wishlist_master,feedback,organization_portfolio_master
# Register your models here.

class role_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'role_name'] 
    

class orgnizer_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'phone_number', 'user_profile_image', 'created_date', 'is_active', 'role','address']

admin.site.register(orgnizer_master, orgnizer_masterAdmin)

 
class category_masterAdmin(admin.ModelAdmin):
    list_display=['id','cat_name'] 
    
class organizer_info_masterAdmin(admin.ModelAdmin):
    list_display=['id',' category',' org_id','  Description',' organization_name','  languages ','  identification',' maxchanges',' minchanges']   
    
class  organization_portfolio_masterAdmin(admin.ModelAdmin):
    list_display=['id','  or_img','org']

class customer_Admin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'phone_number', 'profile_image', 'created_date', 'is_active', 'role']

admin.site.register(customer, customer_Admin)
 
class whoview_masterAdmin(admin.ModelAdmin):
    list_display=['id',' customer','viewed_date','organizer']      
        
class wishlist_masterAdmin(admin.ModelAdmin):
    list_display=['id',' organizer']

class category_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat_name']

class organizer_info_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'org_id', 'Description', 'organization_name', 'languages', 'identification', 'maxchanges', 'minchanges']

class organization_portfolio_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'or_img','org']

class customer_Admin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'phone_number', 'profile_image', 'created_date', 'is_active', 'roles']

class whoview_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'viewed_date', 'organizer']

class wishlist_masterAdmin(admin.ModelAdmin):
    list_display = ['id', 'organizer']

admin.site.register(role_master, role_masterAdmin)
admin.site.register(category_master, category_masterAdmin)
admin.site.register(organizer_info_master, organizer_info_masterAdmin)
admin.site.register(organization_portfolio_master, organization_portfolio_masterAdmin)
admin.site.register(whoview_master, whoview_masterAdmin)
admin.site.register(wishlist_master, wishlist_masterAdmin)

admin.site.register(feedback)