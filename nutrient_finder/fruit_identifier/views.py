import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import openai
import requests
from .forms import SearchForm, FruitImageForm
from .models import FruitVegetable
from .utils import identify_fruit, fetch_nutrients
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from google.cloud import vision
from google.cloud.vision_v1 import types

@csrf_exempt
def image_to_text(request):
        data = json.loads(request.body.decode('utf-8'))
        print("data..",data)
        encoded_image = data.get('image')
        request_payload = {
  "requests": [
    {
      "features": [
        {
          "maxResults": 50,
          "type": "LANDMARK_DETECTION"
        },
        {
          "maxResults": 50,
          "type": "FACE_DETECTION"
        },
        {
          "maxResults": 50,
          "model": "builtin/latest",
          "type": "OBJECT_LOCALIZATION"
        },
        {
          "maxResults": 50,
          "model": "builtin/latest",
          "type": "LOGO_DETECTION"
        },
        {
          "maxResults": 50,
          "type": "LABEL_DETECTION"
        },
        {
          "maxResults": 50,
          "model": "builtin/latest",
          "type": "DOCUMENT_TEXT_DETECTION"
        },
        {
          "maxResults": 50,
          "type": "SAFE_SEARCH_DETECTION"
        },
        {
          "maxResults": 50,
          "type": "IMAGE_PROPERTIES"
        },
        {
          "maxResults": 50,
          "type": "CROP_HINTS"
        }
      ],
      "image": {
        "content": encoded_image
      },
      "imageContext": {
        "cropHintsParams": {
          "aspectRatios": [
            0.8,
            1,
            1.2
          ]
        }
      }
    }
  ]
}
        api_key = 'AIzaSyDBhrpd8Fv0i9WZXWx4wXf_E7-egjmWT_o'
         # Google Vision API endpoint
        api_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        # Send the request to Google Vision API
        response = requests.post(
            api_url,
            # headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            data=json.dumps(request_payload)
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        print(result)
        # Extract text annotations from the response
        texts = result.get('responses', [{}])[0].get('localizedObjectAnnotations', [])
        descriptions = [annotation['name'] for annotation in texts]
        
        # Join descriptions as comma-separated values
        detected_text = ', '.join(descriptions)
        #detected_text = ", ".join([text.get('name') for text in texts])
        print("detected_text....",detected_text)
        gpt_response = get_gpt_response(detected_text)
        print("gpt_response..",gpt_response)
        return HttpResponse(gpt_response)

@csrf_exempt
def text_to_data(request):
     print("request.body.message..",request.body)
     body_unicode = request.body.decode('utf-8')
     data = json.loads(body_unicode)
     input_value = data.get('inputValue', '')
     gpt_response = get_gpt_response(input_value)
     print("gpt_response..",gpt_response)
     return HttpResponse(gpt_response)

def get_gpt_response(prompt):
    print("get_gpt_response", prompt)
    """Call OpenAI API with a prompt and return the response."""
    try:
        openai.api_key = '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'
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if available
        messages= [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Give the full nutritional facts along with vitamins information of only fruits and vegetable in the "+prompt+" in json format without extra text and json structure as {carrot:{calories:12gm,vitaminC:1gm},apple:{calories:10gm,vitaminA:2gm}}"},
            ],
        max_tokens=1000,
        n=1,
        temperature=0.7,
    )   
        print("openAI...", response)
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
   
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
""" 
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
"""