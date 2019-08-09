from django.urls import path,include
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.index,name='home'),
    path('contact/',views.contact,name='contact'),
    path('category/<int:id>/',views.main_category,name='cat'),
    path('category/<int:id>/<int:sid>/',views.sub_category,name='scat'),
    path('product/<int:pid>/',views.mainProduct,name='produ'),
    path('viewcart/<int:id>/',views.view_cart,name='viewcart'),
    path('addcart/<int:pid>/',views.addcart,name='addcart'),
    path('removecart/<int:id>/',views.removecart,name='removecart'),
    path('checkout/',views.checkout,name='checkout'),
    path('handlepayment/',views.handlereuest,name='handlepayment'),
]
