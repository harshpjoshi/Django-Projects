from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class ProfileModel(models.Model):
    '''
        this is Profile creation form
    '''
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='images/')

    def __str__(self):
        return self.user.username

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
