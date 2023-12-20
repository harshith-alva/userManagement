from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User 
from django.contrib import auth
from django.contrib.auth import authenticate,logout,login
from django.db.models import Q


# Create your views here.
@never_cache
def adminlogin(request):
    if "username" in request.session:
        return redirect(home_page)
    if request.method=='POST':
        uname=request.POST.get('user')
        passs=request.POST.get('pas')
        myname=auth.authenticate(username=uname,password=passs)
        if myname is not None and myname.is_superuser:
            request.session['username']=uname
            auth.login(request,myname)
            return redirect(adminhome)
        else:
            messages.error(request,'invalid username and password')
    return render(request,'Adminlogin.html')

@never_cache
def register_page(request):
    # if "username" in request.session:
    #     return redirect(home_page)
    if request.method=='POST':
        yname=request.POST.get('fname')
        email=request.POST.get('email')
        pss=request.POST.get('pass1')
        pss1=request.POST.get('pass2')
        if pss==pss1:
            myname=User.objects.create_user(username=yname,email=email,password=pss)
            myname.save();
            
            if not request.user.is_superuser:
                return redirect(login_page)
            elif request.user.is_superuser:
                return redirect(adminhome)
        else:
            messages.error(request,"password didn't match")

    return render(request,'UserRegistration.html')

@never_cache
def login_page(request):
    if "username" in request.session:
        return redirect(home_page)
    if request.method=='POST':
        uname=request.POST.get('user')
        passs=request.POST.get('pas')
        myname=auth.authenticate(username=uname,password=passs)
        if myname is not None:
            request.session['username']=uname
            auth.login(request,myname)
            return redirect(home_page)
        else:
            messages.error(request,'invalid username and password')
    if not "username" in request.session:
        return render(request,'login.html')
    return render(request,'login.html')

@never_cache
def home_page(request):
    if request.user.is_superuser:
        return redirect (adminhome)
    if 'username' in request.session:
        student = request.session['username']
        return render(request,'home.html',{'user':student})
    return redirect(login_page)

@never_cache
def logout(request):
    if 'username' in request.session:
        request.session.clear()
        return redirect(login_page)
    
@never_cache   
def adminhome(request):
    if not request.session and request.user.is_superuser:
        return redirect(adminlogin)
    myname=User.objects.filter(is_superuser=False)
    udata=[{'id':i.id,'username':i.username,'email':i.email}for i in myname]
    if 'username' in request.session and request.user.is_superuser:
        return render(request,'Adminhome.html',{'user_data':udata})
    else:
        return redirect(adminlogin)
    
@never_cache
def adminlogout(request):
    logout(request)
    request.session.flush()
    return redirect(adminlogin)

@never_cache
def delete_user(request,user_id):
    duser=get_object_or_404(User,pk=user_id)
    if request.user.is_superuser or request.user.has_perm('auth.delete_user'):
        duser.delete()
    else:
        return HttpResponseForbidden("You dont have permission")
    return redirect(adminhome)

@never_cache
def edit_user(request,user_id):
    if not'username' in request.session and request.user.is_superuser:
        return redirect(adminlogin)
    euser=get_object_or_404(User,pk=user_id)
    if 'username' in request.session and request.user.is_superuser:
        if request.method=="POST":
            newname=request.POST.get('user')
            newemail=request.POST.get('email')
            euser.username=newname
            euser.email=newemail
            euser.save();
            return redirect(adminhome)
        return render(request,'edit.html',{'eduser':euser})
    
@never_cache
def search_view(request):
    if not 'username' in request.session and request.user.is_superuser:
        return redirect(adminlogin)
    
    if request.method== 'POST':
        search_query = request.POST.get('search_query') 
        search_results = User.objects.filter(Q(username__icontains=search_query) & Q(is_superuser= False))     
    else:
        search_results = []  # Initialize search_results as an empty list
        
            
    return render(request, 'search.html', {'search_results': search_results})




    

    