from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 100)
	client_type = models.IntegerField(default = 0)
	email = models.EmailField(max_length = 100)
	password = models.CharField(max_length = 100)
	contact = models.CharField(max_length = 100)
	phone = models.CharField(max_length = 10)
	address = models.CharField(max_length = 100)
	descripction = models.CharField(max_length = 1000)
	mision = models.CharField(max_length = 1000)
	vision = models.CharField(max_length = 1000)
	profile_picture = models.ImageField(upload_to = 'profile_pictures/', default = 'default/profile/default.png')

class Product(models.Model):
	name = models.CharField(max_length = 100)
	descripction = models.CharField(max_length = 1000)
	minimum_sale = models.IntegerField(default = 1)
	unit_price = models.FloatField(default = 0.00)

class ImageModel(models.Model):
	product_fk = models.ForeignKey(Product)
	image = models.ImageField(upload_to = 'product_pictures/')

			