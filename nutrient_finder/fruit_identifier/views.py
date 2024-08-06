from django.shortcuts import render
from .forms import SearchForm, FruitImageForm
from .models import FruitVegetable
from .utils import identify_fruit, fetch_nutrients

def search_nutrients(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                fruit = FruitVegetable.objects.get(name=name)
                return render(request, 'nutrients.html', {'fruit': fruit})
            except FruitVegetable.DoesNotExist:
                return render(request, 'search.html', {'form': form, 'error': 'Fruit or vegetable not found'})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})

def upload_image(request):
    if request.method == 'POST':
        form = FruitImageForm(request.POST, request.FILES)
        if form.is_valid():
            fruit_image = form.save()
            fruit_name = identify_fruit(fruit_image.image.path)
            nutrients = fetch_nutrients(fruit_name)
            fruit_image.name = fruit_name
            # Assign nutrients to the fields
            fruit_image.vitamin_c = nutrients.get('Vitamin C', '')
            fruit_image.fiber = nutrients.get('Fiber', '')
            fruit_image.sugar = nutrients.get('Sugar', '')
            fruit_image.calories = nutrients.get('Calories', '')
            fruit_image.protein = nutrients.get('Protein', '')
            fruit_image.fat = nutrients.get('Fat', '')
            fruit_image.carbohydrates = nutrients.get('Carbohydrates', '')
            fruit_image.potassium = nutrients.get('Potassium', '')
            fruit_image.magnesium = nutrients.get('Magnesium', '')
            fruit_image.calcium = nutrients.get('Calcium', '')
            fruit_image.iron = nutrients.get('Iron', '')
            fruit_image.vitamin_a = nutrients.get('Vitamin A', '')
            fruit_image.vitamin_d = nutrients.get('Vitamin D', '')
            fruit_image.vitamin_b6 = nutrients.get('Vitamin B6', '')
            fruit_image.vitamin_b12 = nutrients.get('Vitamin B12', '')
            fruit_image.save()
            return render(request, 'result.html', {'fruit_image': fruit_image})
    else:
        form = FruitImageForm()
    return render(request, 'upload.html', {'form': form})
