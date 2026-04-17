# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.
# class property_type_master(models.Model):
#     prop_id = models.AutoField()
#     proptype=models.CharField( max_length=150)

# class property_details(models.Model):
#     pid=models.AutoField()
#     property=models.ForeignKey(property_type_master, on_delete = models.CASCADE)
#     prop_desc = models.TextField()
#     prop_price = models.BigIntegerField()
#     prop_location = models.CharField(max_length=150)
#     stateId=models.CharField(max_length=150)
#     prop_img=models.FileField(upload_to="Property_img")
#     address = models.TextField()
#     contact_person = models.BigIntegerField()
#     posted_date = models.DateField(auto_now_add=True)
#     prop_d_id = models.ForeignKey(User,on_delete=models.CASCADE)
    
# class property_images(models.Model):
#     img_path= models.URLField( max_length=200)
#     title=models.CharField(max_length=50)
#     prop_d_id = models.ForeignKey(User,on_delete=models.CASCADE)
#     property_id =models.ForeignKey(property_details,on_delete=models.CASCADE)

# class customer_master(models.Model):
#     cid = models.AutoField()
#     username= models.CharField(max_length=50, unique=True)
#     password= models.CharField(max_length=50,)
#     full_name= models.CharField(max_length=150)
#     email= models.EmailField(max_length=254,blank=True, unique=True)
#     phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
#     profile_image= models.ImageField(blank=True,upload_to='profile')
#     created_date = models.DateField(auto_now_add=True)
#     is_active = models.BooleanField(default = False)
    
# class customer_requirements(models.Model):
#     cr_id =models.AutoField()
#     customer=models.ForeignKey(customer_master, on_delete = models.CASCADE)  
#     req_id = models.AutoField()
#     username= models.CharField(max_length=50, unique=True)
#     requirement_details = models.TextField()
#     posted_date = models.DateField(auto_now_add=True)
    
# class engineering_master(models.Model):
#     eng_id =models.AutoField()
#     eng_name = models.CharField(max_length=100)
#     company_name=models.CharField(max_length=100)
#     contact = models.BigAutoField()
#     email=models.EmailField(max_length=100)
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
    
# class quotation_master(models.Model):
#     quotation_id = models.AutoField()
#     quotation_price = models.BigIntegerField()
#     req_id = models.ForeignKey(customer_requirements,on_delete=models.CASCADE)
#     eng_id = models.ForeignKey(engineering_master,on_delete=models.CASCADE)
    

    