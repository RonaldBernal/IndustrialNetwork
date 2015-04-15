# -*- coding: utf-8 -*-
from django import forms
from app.models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Nombre del producto'}
            )
        )
    description = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Descripción del producto'}
            )
        )
    minimum_sale = forms.IntegerField(
        required=True, 
        widget=forms.NumberInput(
            attrs={'class':'form-control', 'placeholder':'Cantidad Mínima de Venta', 'min': '0', 'step': '1', 'value': '0'}
            )
        )
    unit_price = forms.FloatField(
        required=True, 
        widget=forms.NumberInput(
            attrs={'class':'form-control', 'placeholder':'Cantidad Mínima de Venta', 'min': '0', 'step': '0.1', 'value': '0'}
            )
        )
    image = forms.FileField(
        required = False,
        widget = forms.FileInput(
            attrs = {'name':'newProductImage', 'onchange':'PreviewImage();'}
            )
    )

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Product
        fields = ['name', 'description', 'minimum_sale', 'unit_price', 'image']
