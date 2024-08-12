from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_nutrients, name='search_nutrients'),
    path('image-to-text/', views.image_to_text, name='image_to_text'),
    path('text_to_data/', views.text_to_data, name='text_to_data')
]
