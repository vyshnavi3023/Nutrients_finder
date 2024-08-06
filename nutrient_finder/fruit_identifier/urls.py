from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_nutrients, name='search_nutrients'),
    path('upload/', views.upload_image, name='upload_image'),
]
