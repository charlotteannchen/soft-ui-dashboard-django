from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('askWithImage/', views.askWithImage, name='askWithImage'),
    path('questions/', views.questions, name='questions'),
]
