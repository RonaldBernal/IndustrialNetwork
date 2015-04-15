# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    #custom fields
    org_name = models.CharField(max_length = 100, default='')
    client_type = models.IntegerField(default = 0)
    phone = models.CharField(max_length = 10, default='')
    address = models.CharField(max_length = 100, default='')
    description = models.CharField(max_length = 1000, default='')
    mision = models.CharField(max_length = 1000, default='')
    vision = models.CharField(max_length = 1000, default='')
    profile_picture = models.ImageField(upload_to = 'app/media/profile_pictures/', default = 'app/media/default/profile_default.png')

    def __str__(self):
        return self.org_name
    def __unicode__(self):
        return self.org_name

class Product(models.Model):
    client_fk = models.ForeignKey(Client)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 1000)
    minimum_sale = models.IntegerField(default = 1)
    unit_price = models.FloatField(default = 0.00)
    image = models.ImageField(upload_to = 'app/media/product_pictures/', default = 'app/static/assets/img/image.png')

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name