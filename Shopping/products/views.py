from django.shortcuts import render,redirect
from .forms import ContactForm,OrderForm
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import MainCategory,SubCategory,Product,Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from Paytm import checksum
# Create your views here.

def index(request):
    main_cat = MainCategory.objects.all()
    products = Product.objects.all()[:6]
    uid =request.user.id
    cart = Cart.objects.filter(user=uid).count()
    return render(request,'products/index.html',{'maincat':main_cat,'product':products,'cart_count':cart})

def contact(request):
    main_cat = MainCategory.objects.all()
    cart = Cart.objects.filter(user=request.user.id).count()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            mesage = form.cleaned_data['message']
            try:
                send_mail(subject,mesage,from_email,['harshjoshi989@gmail.com'])
                messages.success(request, 'Successfully Sent.')
            except BadHeaderError:
                return HttpResponse('Bad Header')
            return redirect('products:contact')
    else:
        form = ContactForm()
    return render(request,'products/contact.html',{'form':form,'maincat':main_cat,'cart_count':cart})

def main_category(request,id):
    cart = Cart.objects.filter(user=request.user.id).count()
    scat = SubCategory.objects.filter(main_cat=id)
    main_cat = MainCategory.objects.all()
    mcat = MainCategory.objects.get(id=id)
    products = Product.objects.all()
    return render(request,'products/category.html',{'mcat':mcat,'maincat':main_cat,'subcat':scat,'cart_count':cart})

def sub_category(request,id,sid):
    cart = Cart.objects.filter(user=request.user.id).count()
    scat = SubCategory.objects.filter(main_cat=id)
    main_cat = MainCategory.objects.all()
    prod = Product.objects.filter(subcat=sid)
    print(scat)
    return render(request,'products/category.html',{'maincat':main_cat,'subcat':scat,'prod':prod,'cart_count':cart})

def mainProduct(request,pid):
    cart = Cart.objects.filter(user=request.user.id).count()
    main_cat = MainCategory.objects.all()
    product1 = Product.objects.get(id=pid)
    return render(request,'products/product.html',{'prod1':product1,'maincat':main_cat,'cart_count':cart})

@login_required
def view_cart(request,id):
    cart = Cart.objects.filter(user=request.user.id).count()
    main_cat = MainCategory.objects.all()
    products = Cart.objects.filter(user=id).all()
    total = Cart.objects.filter(user=id).aggregate(Sum('totalprice'))
    print("Total is: ",total)
    return render(request,'products/cart.html',{'maincat':main_cat,'products':products,'cart_count':cart,'total':total})

@login_required
def addcart(request,pid):
    cart = Cart.objects.filter(user=request.user.id).count()
    main_cat = MainCategory.objects.all()
    uid = request.user
    qty = request.POST.get('qty')
    prodid = Product.objects.get(id=pid)
    price = int(prodid.price) * int(qty)
    prod = Cart(product=prodid,user=uid,quantity=qty,totalprice=price)
    prod.save()
    return redirect('products:home')

@login_required
def removecart(request,id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    uid=request.user.id
    return redirect(reverse('products:viewcart',kwargs={'id':uid}))

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user.id).count()
    main_cat = MainCategory.objects.all()
    idata = Cart.objects.filter(user=request.user).values()
    id = request.user.id
    products = Cart.objects.filter(user=id).all()
    total = Cart.objects.filter(user=id).aggregate(Sum('totalprice'))
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.items = [x for x in idata]
            print("Items ....",idata)
            profile.save()
            print("Email",profile.user.email)
            print("Rs",total['totalprice__sum'])
            print("Order id",profile.pk)
            print('Successfully.....')

            param_dict ={
            'MID':'Merchant id',
            'ORDER_ID':str(profile.pk),
            'TXN_AMOUNT':str(total['totalprice__sum']),
            'CUST_ID':profile.user.email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/handlepayment/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,'uAnxa&YsJFT_pqcQ')
        print('Cheall',param_dict)
        return render(request,'products/paytm.html',{'pram_dict':param_dict})
    else:
        form = OrderForm()
    #request paytm to accept to ammount to your account
    return render(request,'products/checkout.html',{'maincat':main_cat,'cart_count':cart,'form':form,'products':products,'total':total})

@csrf_exempt
def handlereuest(request):
    #paytm sent post request and csrf_exempt is remove that time
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksumf = form[i]
    verify = checksum.verify_checksum(response_dict,'Merchant key',checksumf)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order Successfull")
        else:
            print("Order Not Successfull bescause ",response_dict['RESPMSG'])
    return render(request,'products/paymentstatus.html',{'response':response_dict})
