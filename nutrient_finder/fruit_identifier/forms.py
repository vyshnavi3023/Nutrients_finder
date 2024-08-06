from django import forms
from .models import FruitVegetable

class SearchForm(forms.Form):
    name = forms.CharField(label='Fruit or Vegetable Name', max_length=100)

class FruitImageForm(forms.ModelForm):
    class Meta:
        model = FruitVegetable
        fields = ['name']
