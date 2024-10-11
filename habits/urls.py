from django.urls import path
from . import views

urlpatterns = [
    path('create_habit', views.create_habit, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
]