from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserResgister,UserUpdate,ProfileUpdate
from django.contrib.auth.decorators import login_required
from products.models import Product,MainCategory,SubCategory

# Create your views here.

def register(request):

    ''' this is for register user it can use UserRegister Model'''

    main_cat = MainCategory.objects.all()
    if request.method == 'POST':
        form = UserResgister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created For {username}')
            return redirect('products:home')
    else:
        form = UserResgister()
    return render(request,'users/register.html',{'form':form,'maincat':main_cat})

@login_required
def profile(request):

    ''' this for updating and displaying Userprofile '''

    main_cat = MainCategory.objects.all()

    if request.method == 'POST':
        u_form = UserUpdate(request.POST,instance=request.user)
        p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profilemodel)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile is Updated')
            return redirect('users:profile')
    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profilemodel)
    return render(request,'users/profile.html',{'maincat':main_cat,'u_form':u_form,'p_form':p_form})
