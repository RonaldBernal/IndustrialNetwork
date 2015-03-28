from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length = 100, default='')
    client_type = models.IntegerField(default = 0)
    
    email = models.EmailField(max_length = 100,  unique=True, db_index=True)
    #joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    contact = models.CharField(max_length = 100, default='')
    phone = models.CharField(max_length = 10, default='')
    address = models.CharField(max_length = 100, default='')
    descripction = models.CharField(max_length = 1000, default='')
    mision = models.CharField(max_length = 1000, default='')
    vision = models.CharField(max_length = 1000, default='')
    profile_picture = models.ImageField(upload_to = 'app/media/profile_pictures/', default = 'app/media/default/profile_default.png')

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 100)
    descripction = models.CharField(max_length = 1000)
    minimum_sale = models.IntegerField(default = 1)
    unit_price = models.FloatField(default = 0.00)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
        
class ImageModel(models.Model):
    product_fk = models.ForeignKey(Product)
    image = models.ImageField(upload_to = 'app/media/product_pictures/', default = 'app/media/default/product_default.png')
    imageName = image.name
    
    def __str__(self):
        return u'%s_%s' % (self.product_fk, self.imageName)
    def __unicode__(self):
        return u'%s_%s' % (self.product_fk, self.imageName)