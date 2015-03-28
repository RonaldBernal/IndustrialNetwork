from django import forms
from app.models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(label="Producto")
    descripction = forms.CharField(label="Descripcion")
    minimum_sale = forms.IntegerField()
    unit_price = forms.FloatField()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Product
        fields = ['name', 'descripction', 'minimum_sale', 'unit_price']
