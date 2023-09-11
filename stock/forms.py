from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['label']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProductNewForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'category', 'description', 'unit', 'cost', 'price', 'quantity', 'enabled']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'qunatity': forms.NumberInput(attrs={'class': 'form-control'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'category', 'unit', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }


class ProductStockForm(forms.ModelForm):
    ACTIONS = [
        ('no', 'No action'),
        ('add', 'Add to stock'),
        ('rem', 'Remove from stock')
    ]
    action = forms.ChoiceField(label='Action', help_text='Select Action', initial='no', required=True, widget=widgets.RadioSelect(), choices=ACTIONS)
    add_qty = forms.IntegerField(label='Quantity to add/remove', help_text='Select quantity to add/remove', initial=0, required=True, widget=widgets.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Product
        fields = ['enabled', 'cost', 'price', 'action', 'add_qty']
        labels = {
            'enabled': 'Enable this product in stock',
            'cost': 'Stock cost of this product',
            'price': 'Price of this product'
        }
        widgets = {
            'enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_add_qty(self):
        qty = self.cleaned_data['add_qty']
        act = self.cleaned_data['action']
        if act != 'no':
            if qty < 1:
                raise ValidationError('Invalid quantity! Must be at least 1')
            elif act == 'rem' and qty > self.instance.quantity:
                raise ValidationError('Invalid quantity! Must be less than or equal to stock quantity')
        return qty