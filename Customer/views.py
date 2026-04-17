
from urllib import request
from django.shortcuts import render,HttpResponseRedirect,redirect
from DataAccess.models import customer, wishlist_master ,category_master,organizer_info_master,whoview_master ,orgnizer_master
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.db.models import Q
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

# # Create your views here.

def custadmin(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/Customer/cust_login')

    # Retrieve the user object based on the user_id stored in the session
    user = customer.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        try:
            service = category_master.objects.all()
            organizer = organizer_info_master.objects.all()
            
            if request.method == "POST":
                Category1 = request.POST.get('category')
                location1 = request.POST.get('location')
                Taluka1 = request.POST.get('Taluka')
                print(Category1, location1, Taluka1)
                
                if 'submit' in request.POST and request.POST['submit'] == 'Search':
                    print("search")
                    # Check if any of the search criteria are None
                    if Category1 is None or location1 is None or Taluka1 is None:
                        # Handle the case where any search criteria are missing
                        messages.error(request, "Please provide all search criteria.")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        if Category1 is not None or location1 is None or Taluka1 is None:
                            # Perform the search query
                            organizer = organizer.filter(
                                Q(category__cat_name__icontains=Category1) 
                            )
                        elif Category1 is not None or location1 is not None or Taluka1 is not None:
                            organizer = organizer.filter(
                                Q(category__cat_name__icontains=Category1) |
                                Q(org_id__address__icontains=location1) 
                            )
                       
                        context = {"service": service, "organizer": "organizer","uid":user}
  
            if request.method == "POST":
                organizerid = request.POST.get('oid')
                customerid = request.POST.get('cid')
                cobj = customer.objects.get(pk=customerid)
                Oobj = orgnizer_master.objects.get(pk=organizerid)
                print(organizerid, customerid)
                if organizerid and customerid is not None:
                    view = whoview_master.objects.create(customer=cobj, organizer=Oobj, viewed_date=date.today())
                    view.save()
                else:
                    messages.error(request, "")
                
            if 'submit' in request.POST and request.POST['submit'] == 'view':
                return redirect(f"/Organizer/orginfo/{organizerid},{customerid}")
            
            wish = wishlist_master.objects.all()
            context = {"service": service, "organizer": organizer, "uid": user, "wish": wish}
            
        except ObjectDoesNotExist:
            pass  # Handle the case where the customer with the specified ID does not exist

    context = {"service": service, "organizer": organizer, "uid": user}
    return render(request, "customer/custAdmin.html", context)


def cust_register(request):
    if request.method =="POST":
        username=request.POST.get('username')
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        profile_image=request.FILES.get('profile_image')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        is_active=request.POST.get('is_active')
        print(username,full_name,email,phone_number,profile_image,password,cpassword,is_active)

        cust=customer.objects.filter(username = username)
        if cust.exists():
            messages.error(request,'Email is Already taken')
            return HttpResponseRedirect(request.path_info)
        elif password != cpassword:
            messages.error(request,"Password does not match")
            return HttpResponseRedirect(request.path_info)
        else:  
           cust=customer.objects.create(
                  full_name=full_name,profile_image=profile_image,
                  username=username,phone_number=phone_number,
                  email=email,password=password, 
                )
        if is_active == 'is_active':
            cust.is_active = True
        cust.save()
        messages.success(request,"your account created successfully.")
        return redirect("/Customer/cust_login")
            
    return render(request,"customer/cust_register.html")

def profile(request):
    uid= request.session.get('user_id')
    if not uid:
        return redirect('/Customer/cust_login')
    user = customer.objects.filter(pk=uid).first()
    if uid: 
        if request.method =="POST":
            username=request.POST.get('username')
            full_name=request.POST.get('full_name')
            email=request.POST.get('email')
            phone_number=request.POST.get('phone_number')
            profile_image=request.FILES.get('profile_image')
            is_active=request.POST.get('is_active')
            
            if 'submit' in request.POST and request.POST['submit'] == 'Update':
                user.full_name=full_name
                user.phone_number=phone_number
                user.email=email
                user.username=username
                user.profile_image=profile_image
                if is_active == 'is_active':
                    user.is_active = True
                else:
                    user.is_active = False
                user.save()
                messages.success(request,"your account Updated successfully.")
                return redirect(f'/Customer/custadmin')

            if 'submit' in request.POST and request.POST['submit'] == 'cancel':
                messages.success(request,"your account can not Updated successfully.")
                return redirect(f'/Customer/custadmin')
        else:
            messages.success(request,"your account can not Updated.")
           
    context = {"uid":user,"idr":user}
    return render(request,"customer/cust_register.html",context)

def cust_login(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
    
        if not customer.objects.filter(username=username1).exists():
            messages.error(request,"Invalid Username ")
            return redirect('/Customer/cust_login') 
        
        usern = customer.objects.filter(username=username1).exists()
        if usern == True:
            user=customer.objects.get(username=username1)
            if user.password == password1:
                request.session['user_id'] = user.pk
                request.session['user_email'] = user.email
                return redirect(f"/Customer/custadmin")
            else:
                messages.error(request,"Wronge Password.")

    return render(request,"customer/cust_login.html")

def cust_logout(request): 
    request.session.flush()  
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')

def cust_forgetPass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                orgnizer=customer.objects.filter(email = email)
                if orgnizer.exists():
                    org = customer.objects.get(email=email)
                    
                    subject = "Welcome to Django Wdding PLanner Pro...!!"
                    message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [org.email]
                    send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",org)
                
                    context = {"org":org}
                    return render(request,"customer/cust_forgetPass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect("/host/host_forgetPass")
                    
        elif 'submit' in request.POST and request.POST['submit'] == 'Reset':
                print("reset")
                if request.method == "POST":
                    new_email = request.POST.get('email')
                    new_pass =request.POST.get('password')
                    cpass = request.POST.get('cpassword')
                    print(email,new_pass,cpass)
                        
                    if email is not None:
                     # Update the password
                        if customer.objects.filter(email=new_email).exists():
                            org= customer.objects.get(email=new_email)
                            if new_pass == cpass:
                                org.password = new_pass
                                org.save()
                            else:
                                messages.error(request,"Password does not match")
                                return HttpResponseRedirect("/Customer/cust_forgetPass")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/Customer/cust_forgetPass")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/Customer/cust_forgetPass")
                    else:
                            messages.error(request, "Email is required for the Change Password.")
                            return HttpResponseRedirect(request.path_info)
    return render(request,"customer/cust_forgetPass.html")

def Wishlist(request):  
    uid= request.session.get('user_id')
    if not uid:
        return redirect('/Customer/cust_login')
    user = customer.objects.filter(pk=uid).first()
    if uid:
        if request.method == "POST":
                oid = request.POST.get('id')
        if 'submit' in request.POST and request.POST['submit'] == 'remove':
            if oid is not None:
                print(id)
                if wishlist_master.objects.filter(pk = oid).exists():
                    oid = wishlist_master.objects.get(pk = oid)
                    oid.delete()
                    messages.error(request,"Successfully remove from wish list..!")
            else:
                messages.error(request,"can not remove organizer.")
                return HttpResponseRedirect(requrest.path_info)

    wish = wishlist_master.objects.all() 
    organizer = organizer_info_master.objects.all()  
    context = { "organizer" :organizer,"wish":wish, "uid":user}
    return render(request,'customer/wishlist.html',context)

