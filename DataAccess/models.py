
from django.db import models

# Create your models here.
class role_master(models.Model):
    role_name=models.CharField(max_length=100)
    def __str__(self):
        return self.role_name
   
def get_rol_org():
    return role_master.objects.get(id=3) 
 
 
class orgnizer_master(models.Model):
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    user_profile_image= models.ImageField(blank=True,upload_to='profile')
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    role = models.ForeignKey(role_master,default = get_rol_org, on_delete = models.CASCADE)
    address = models.TextField(blank=True, null=True)
    
    
class category_master(models.Model):
    cat_name = models.CharField(max_length = 150)
    def __str__(self):
        return self.cat_name

class organizer_info_master(models.Model):
    category = models.ForeignKey(category_master,on_delete = models.CASCADE)
    org_id=models.ForeignKey(orgnizer_master,on_delete = models.CASCADE)
    Description = models.TextField()
    organization_name = models.CharField(max_length = 150)
    languages = models.CharField(max_length = 20, blank=True,null=True)
    identification = models.FileField(upload_to="IdentificationFiles")
    maxchanges = models.CharField(max_length = 20,blank=True,null = True)
    minchanges = models.CharField(max_length = 20,blank=True,null = True)
  
def get_org_id():
    return orgnizer_master.objects.get(id=1)  
  
class organization_portfolio_master(models.Model):
    or_img = models.FileField(upload_to="OrganizationPortfolio")
    org = models.ForeignKey(orgnizer_master,default = get_org_id, on_delete = models.CASCADE)
  
def get_rol_cust():
    return role_master.objects.get(id=2)
 
class customer(models.Model):
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    profile_image= models.ImageField(blank=True,upload_to='profile')
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    role = models.ForeignKey(role_master,default = get_rol_cust, on_delete = models.CASCADE)
    
   
class whoview_master(models.Model):
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    viewed_date = models.DateField(auto_now=True)
    organizer = models.ForeignKey(orgnizer_master,on_delete=models.CASCADE)
    
class wishlist_master(models.Model):
    organizer = models.ForeignKey(orgnizer_master,on_delete = models.CASCADE)    
    
class feedback(models.Model):
    name = models.CharField(max_length = 100)
    email =models.EmailField(max_length = 150)
    subject = models.CharField(max_length=200)
    message = models.TextField() 



    