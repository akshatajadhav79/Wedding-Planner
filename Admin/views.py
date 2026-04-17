from django.shortcuts import render,HttpResponseRedirect,redirect
from DataAccess.models import category_master,feedback,organizer_info_master,orgnizer_master,organization_portfolio_master
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,logout,login
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def base(request):
    service = category_master.objects.all()
    context = {"service":service}
    return render(request,"mainweb/home.html",context)

@login_required(login_url='/adminLogin')
def hostadmin(request):
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
               
                messages.success(request, "Search Completed!")
                context = {"service": service, "organizer": "organizer"}
  
        
        if 'submit' in request.POST and request.POST['submit'] == 'view':
            if request.method == "POST":
                oid = request.POST.get('oid')
                return redirect(f"/Toactivate/{oid}")
        
    context = {"service": service, "organizer": organizer}
    return render(request,"admin/host_admin.html",context)

def logout_admin(request):
    logout(request)
    request.session.flush()
    messages.success(request,"Log out Successfully")
    return HttpResponseRedirect('/')
    
def adminLogin(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password= request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Username ")
            return redirect('/adminLogin/') 
        
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,"Invalid Password ")
            return redirect('/adminLogin/')
        
        else:
            #session method use to store user
            login(request,user) 
            request.session['user_id'] = user.pk
            return redirect('/hostadmin')
    return render(request,"admin/adminLogin.html")

def service(request):
    service = category_master.objects.all()
    organizer = organizer_info_master.objects.all()
    print(organizer)
    
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
                       
                        messages.success(request, "Search Completed!")
                        context = {"service": service, "organizer": "organizer"}
            
    context = {"service":service,"organizer":organizer}
    return render(request,"mainweb/service.html",context,)

def Contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        if name and email and subject and message is not None:
            Contact=feedback.objects.create(name=name,email=email,subject=subject,message=message)
            Contact.save()
            messages.error(request,"Thanks for your feedback..!")
        else:
            messages.error(request,"Enter All information")
            
    
    service = category_master.objects.all()
    context = {"service":service}
    return render(request,"mainweb/Contact.html",context)

@login_required(login_url='/adminLogin')
def create_categoty(request):
    if request.method=="POST":
        cat_name=request.POST.get('cat_name')
        id = request.POST.get('id')
        
        
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            print("save")
            if category_master.objects.filter(cat_name=cat_name).exists():
                messages.error(request,"Category is Already exsist..!")
                return HttpResponseRedirect(request.path_info)
            else:       
                category_master.objects.create(cat_name=cat_name )
                messages.success(request,"Category is created successfully")
                
        elif 'submit' in request.POST and request.POST['submit'] == 'cancel':
            print('cancel')
            return HttpResponseRedirect(request.path_info)
        
        elif 'submit' in request.POST and request.POST['submit'] == 'delete':
            if id:
                print(id)
                st = category_master.objects.get(pk=id)
                st.delete()
                messages.success(request, "Category is deleted successfully")
                
        elif 'submit' in request.POST and request.POST['submit'] == 'Edit':
            if id is not None:
                # Retrieve the staff Category to update
                Category = category_master.objects.get(pk=id)
                print("pk=",Category)
                
                # Get the current name of the staff Category
                current_name =Category.cat_name
                print(current_name)
                
                Category = category_master.objects.all()
                context = {"Category":Category,"cat_name": current_name,"id":id }
                return render(request, "admin/category.html", context)
            
      
        elif 'submit' in request.POST and request.POST['submit'] == 'update':
                print("update")
                if id is not None:
                    print(id)
                    Category = category_master.objects.get(pk=id)
                    print("pk=", Category)
                    if request.method == "POST":
                        new_name = request.POST.get('cat_name')
                        print(new_name)
                        
                        if new_name is not None:
                            # Update the name of the staff Category
                            Category.cat_name = new_name
                            Category.save()
                            messages.success(request, "Category is updated successfully")
                            return HttpResponseRedirect("/create_categoty")
                        else:
                            messages.error(request, "New Category is required for the update.")
                            return HttpResponseRedirect(request.path_info)
                               
                Category = category_master.objects.all()
                context = {"Category":Category,"cat_name": current_name,"id":id ,}
                return render(request, "admin/category.html",context)
            
    Category = category_master.objects.all()
    context = {"Category":Category}
    return render(request,"admin/category.html",context)


def bothlogin(request):
    service = category_master.objects.all()
    context = {"service":service}
    return render(request,"mainweb/bothLogin.html",context)

@login_required(login_url='/adminLogin')
def activate_planner(request):
    if request.method == "POST":
        oid = request.POST.get('oid')
        print(oid)

    if 'submit' in request.POST and request.POST['submit'] == 'activate':
        if oid is not None:
            if orgnizer_master.objects.filter(id = oid).exists():
                organizerid = orgnizer_master.objects.get(pk=oid)
                organizerid.is_active = True
                organizerid.save()
                messages.success(request,"Successfully Deacivate..!")

            else:
                messages.error(request,"Not Deactivate sorry")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request,"Not Deactivate sorry..!")

    if 'submit' in request.POST and request.POST['submit'] == 'deactivate':
        if oid is not None:
            if orgnizer_master.objects.filter(id = oid).exists():
                organizerid = orgnizer_master.objects.get(pk=oid)
                organizerid.is_active = False
                organizerid.save()
                messages.success(request,"Successfully Deacivate..!")
                    
            else:
                messages.error(request,"Not Deactivate sorry")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request,"Not Deactivate sorry..!")
    organizer = orgnizer_master.objects.all()
    context = {"organizer":organizer}
    return render(request,"admin/Activate_planner.html",context)

@login_required(login_url='/adminLogin')
def Toactivate(request,id):
    if id:
        print(id)
        organizer = organizer_info_master.objects.get(org_id=id)
        port = organization_portfolio_master.objects.all()
        if request.method == "POST":
            oid = request.POST.get('oid')
            print(oid)

    if 'submit' in request.POST and request.POST['submit'] == 'activate':
            print("cs")
            if oid is not None:
                if orgnizer_master.objects.filter(id = oid).exists():
                    organizerid = orgnizer_master.objects.get(pk=oid)
                    organizerid.is_active = True
                    organizerid.save()
                    messages.success(request,"Successfully Acivate..!")
                        
                else:
                    messages.error(request,"sorry Not Activate.")
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request,"Not Activate sorry..!")

    if 'submit' in request.POST and request.POST['submit'] == 'deactivate':
        if oid is not None:
            if orgnizer_master.objects.filter(id = oid).exists():
                organizerid = orgnizer_master.objects.get(pk=oid)
                organizerid.is_active = False
                organizerid.save()
                messages.success(request,"Successfully Deacivate..!")
                    
            else:
                messages.error(request,"Not Deactivate sorry")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request,"Not Deactivate sorry..!")
    context = {"organizer":organizer,"port":port}
    return render(request,"admin/Toactivate.html",context)

