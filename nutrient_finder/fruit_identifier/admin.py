import json
from django.contrib import admin
from .models import FruitVegetable


from django.contrib import admin
from .models import FruitVegetable

@admin.register(FruitVegetable)
class FruitVegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'vitamin_c', 'fiber', 'sugar', 'calories', 'protein', 'fat', 'carbohydrates', 'potassium', 'magnesium', 'calcium', 'iron', 'vitamin_a', 'vitamin_d', 'vitamin_b6', 'vitamin_b12')
    search_fields = ('name',)
