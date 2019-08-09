from django.db import models
from django.urls import reverse
from PIL import Image
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class MainCategory(models.Model):
    main_cat = models.CharField(max_length=100)

    def __str__(self):
        return self.main_cat

class SubCategory(models.Model):
    main_cat = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subcat = models.TextField(max_length=200)

    def __str__(self):
        return self.subcat

class Product(models.Model):
    subcat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='images/')
    name = models.TextField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:produ',kwargs={'pid':self.id})

    def get_absolute_url_addcart(self):
        return reverse('products:addcart',kwargs={'pid':self.id})

    def save(self):
        super().save()
        '''
            resize the profile image
        '''
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output = (300,300)
            img.thumbnail(output)
            img.save(self.image.path)

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    totalprice = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name;

    def get_absolute_url_removecart(self):
        return reverse('products:removecart',kwargs={'id':self.id})

    def get_absolute_url_viewcart(self):
        return reverse('products:viewcart',kwargs={'id':self.user.id})

class Order(models.Model):
    items = models.TextField(max_length=1500)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.TextField(max_length=300)
    zipcode = models.IntegerField()
    mobile = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
