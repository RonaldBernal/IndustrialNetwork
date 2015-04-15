# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class ProductInLine(admin.TabularInline):
	model = Product

class ClientAdmin(admin.ModelAdmin):
	inlines = (ProductInLine, )

admin.site.register(Client, ClientAdmin)
admin.site.register(Product)
