from urllib import request
from django.shortcuts import render,HttpResponseRedirect,redirect
from DataAccess.models import customer, organizer_info_master,orgnizer_master,category_master,whoview_master,organization_portfolio_master,wishlist_master
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.db.models import Q , Count


# Create your views here.
def Orgadmin(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary

    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/Organizer/org_login')

    # Retrieve the user object based on the user_id stored in the session
    user = orgnizer_master.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        return render(request, "org/orgAdmin.html", {'uid': user})
    else:
        # User does not exist, handle accordingly (redirect, show error, etc.)
        messages.error(request, "User not found.")
        return redirect('/Organizer/org_login')

def org_register(request):
    if request.method =="POST":
        username=request.POST.get('username')
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        
        org=orgnizer_master.objects.filter(email = email)
        if org.exists():
            messages.error(request,'Email is Already taken')
            return HttpResponseRedirect(request.path_info)
        elif password != cpassword:
            messages.error(request,"Password does not match")
            return HttpResponseRedirect(request.path_info)
        else:  
            org=orgnizer_master.objects.create(
                    full_name=full_name,
                    username=username,
                    email=email,password=password, 
                )
       
        org.save()
        messages.success(request,"your account created successfully.")
        return redirect("/Organizer/org_login")
            
    return render(request,"org/org_register.html")

def org_login(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
        if 'submit' in request.POST and request.POST['submit'] == 'Login':
            if username1 is None or password1 is None or username1 == '' or password1 == '':
                messages.error(request,"Please Enter Username and Password")
            else:
                if not orgnizer_master.objects.filter(username=username1).exists():
                    messages.error(request,"Invalid Username ")
                    return redirect('/Organizer/org_login') 
                
                usern = orgnizer_master.objects.filter(username=username1).exists()
                if usern == True:
                    user=orgnizer_master.objects.get(username=username1)
                    if user.password == password1:
                        request.session['user_id'] = user.pk
                        request.session['user_email'] = user.email
                        id = int(user.id)
                        return redirect(f"/Organizer/Orgadmin")
                    else:
                        messages.error(request,"Wronge Password.")

    return render(request,"org/org_login.html")


def Org_logout(request): 
    request.session.flush()    
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')

def org_profile(request):
    uid= request.session.get('user_id')
    if not uid:
        return redirect('/Organizer/org_login')
    user = orgnizer_master.objects.filter(pk=uid).first()
    if uid: 
        ct = category_master.objects.all()

        if request.method == "POST":
            # Retrieve form data organizer_master
            username = request.POST.get('username')
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            user_profile_image = request.FILES.get('user_profile_image')
            print(user_profile_image)
            address = request.POST.get('address')
            
            # for organizer_info_master data save
            organization_name1=request.POST.get('organization_name')
            org_id1=user
            Description1=request.POST.get('Description')
            languages1=','.join(request.POST.getlist('languages'))
            identification1=request.FILES.get('identification')
            category_id=request.POST.get('category')
            
            # Check if the submit button is for updating
            if 'submit' in request.POST and request.POST['submit'] == 'Update':
                # Update user object with form data
                user.username = username
                user.full_name = full_name
                user.email = email
                user.phone_number = phone_number
                user.address = address
                if user_profile_image is None:
                    messages.error(request,"user Image must be uploaded..!")
                else:
                    user.user_profile_image = user_profile_image
                    

                # Save the changes to the database
                user.save()
                # Retrieve category_master instance based on category_id
                if category_id is None or category_id=="":
                    messages.error(request,"Please enter category..!")
                else:
                    category = get_object_or_404(category_master, pk=category_id)
                 
                    # Create or update organizer_info_master object
                    org, created = organizer_info_master.objects.get_or_create(
                        org_id=org_id1,
                        defaults={
                            'Description': Description1,
                            'organization_name': organization_name1,
                            'identification': identification1,
                            'category': category
                        }
                    )
                    # org.languages.set(languages1)
                    org.languages = languages1
                    org.save()

                    # Provide feedback to the user
                    if created:
                        messages.success(request, "Organizer information updated successfully!")
            else:
                messages.success(request, "Organizer information Not updated sorry!")
                
        if 'submit' in request.POST and request.POST['submit'] == 'Cancel':
                print("cdsd")
                return redirect(f"/Organizer/Orgadmin")

    context = {"uid": user,"user":user,"ct":ct}
    return render(request,"org/org_profile.html",context)
         
def organization(request):
    uid= request.session.get('user_id')
    if not uid:
        return redirect('/Organizer/org_login')
    user = orgnizer_master.objects.filter(pk=uid).first()
    if uid: 
        if request.method == "POST":
            # Retrieve form data organizer_master
            or_img = request.FILES.get('or_img')
            org = request.POST.get('org')
            orgObj = orgnizer_master.objects.get(pk=org)
            if or_img  is not None:
                if 'submit' in request.POST and request.POST['submit'] == 'save':
                    org_img = organization_portfolio_master.objects.create(or_img=or_img, org=orgObj)
                    org_img.save()
                    messages.success(request,"Successfully Uploaded..!")
                
            else:
                messages.error(request,"please upload image")
        
    context = {"uid": user}
    return render(request,"org/organization.html",context)

def org_forgetPass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                orgnizer=orgnizer_master.objects.filter(email = email)
                if orgnizer.exists():
                    org = orgnizer_master.objects.get(email=email)
                    
                    subject = "Welcome to Django Wdding PLanner Pro...!!"
                    message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [org.email]
                    send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",org)
                
                    context = {"org":org}
                    return render(request,"org/org_forgetPass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect(request.path_info)
      
        elif 'submit' in request.POST and request.POST['submit'] == 'Reset':
                print("reset")
                if request.method == "POST":
                    new_email = request.POST.get('email')
                    new_pass =request.POST.get('password')
                    cpass = request.POST.get('cpassword')
                    print(email,new_pass,cpass)
                        
                    if email is not None:
                     # Update the password
                        if orgnizer_master.objects.filter(email=new_email).exists():
                            org= orgnizer_master.objects.get(email=new_email)
                            if new_pass == cpass:
                                org.password = new_pass
                                org.save()
                            else:
                                messages.error(request,"Password does not match")
                                return HttpResponseRedirect("/Organizer/org_forgetPass/")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/Organizer/org_forgetPass/")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/Organizer/org_forgetPass/")
                    else:
                            messages.error(request, "Email is required for the Change Password.")
                            return HttpResponseRedirect(request.path_info)
                               
                return render(request, "org/org_forgetPass.html")
            
        
    return render(request,"org/org_forgetPass.html")

def orginfo(request,oid ,cid):
    if oid:
        print(oid)
        organizer = organizer_info_master.objects.get(org_id=oid)
        uid = customer.objects.get(pk=cid)
       
        if request.method=="POST":
            organizerid = request.POST.get('oid')
            cid = request.POST.get('cid')
            print(organizerid)
            if 'submit' in request.POST and request.POST['submit'] == 'cart':
                print("cs")
                if organizerid is not None:
                    if wishlist_master.objects.filter(organizer_id = organizerid).exists():
                        messages.error(request,"Already in the wishlist..!")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        wishlist_entry = wishlist_master.objects.create(organizer_id=organizerid)
                        wishlist_entry.save()
                        messages.success(request,"Successfully Added to cart..!")
                else:
                    messages.error(request,"Not added sorry..!")
            
    port = organization_portfolio_master.objects.all()
    service = category_master.objects.all()
    context = {"organizer":organizer,"service":service,"port":port ,"uid":uid}
    return render(request,"mainweb/orginfo.html",context)

def whoview(request):
    uid= request.session.get('user_id')
    if not uid:
        return redirect('/Organizer/org_login')
    user = orgnizer_master.objects.filter(pk=uid).first()
    if uid:
        # Retrieve the logged-in user's organizer
        cust = customer.objects.all()

        customer_view_counts = whoview_master.objects.filter(organizer_id=uid).values('customer').annotate(view_count=Count('customer'))

        for item in customer_view_counts:
            print("Customer:", item['customer'], "View Count:", item['view_count'])

        views = whoview_master.objects.filter(organizer_id=uid)
        num_customers = views.values('customer').distinct().count()

    context = {"uid": user ,"cust":cust,"customer_view_counts":customer_view_counts ,"num_customers":num_customers}
    return render(request,"org/whoview.html",context)