from django import forms
from django.forms import ModelForm, Textarea, TextInput, ChoiceField
from .models import Partner, Menu

class PartnerForm(ModelForm):
    category = forms.ChoiceField(choices=Partner.CATEGORY_CHOICES)
    class Meta:
        model = Partner
        fields = (
            "name",
            "contact",
            "address",
            "description",
            "category",
        )
        widgets = {
            "name": TextInput(attrs={"class":"form-control"}),
            "contact": TextInput(attrs={"class":"form-control"}),
            "address": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            # "category": ChoiceField(attrs={"class":"form-control"}),
        }

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = (
            "image",
            "name",
            "price",
        )
        widgets = {
            # "image": TextInput(attrs={"class":"form-control"}),
            "name": TextInput(attrs={"class":"form-control"}),
            "price": TextInput(attrs={"class":"form-control"}),
        }
