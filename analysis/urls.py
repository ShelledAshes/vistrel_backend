from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-video/', views.upload_video, name='upload_video'),
]