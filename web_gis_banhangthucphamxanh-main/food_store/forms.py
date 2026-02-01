from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Đổi 'stock' thành 'stock_quantity' ở đây
        fields = ['name', 'category', 'farm', 'price', 'unit', 'description', 'image', 'stock_quantity', 'is_available']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'farm': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}), # Đổi ở đây nữa
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }