from django.urls import path
from . import views

urlpatterns = [
    path('habit_analysis', views.habit_analysis, name='habit_analysis'),
    path('delete_habit/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('create_habit', views.create_habit, name='create_habit'),
    path('dashboard', views.dashboard, name='dashboard'),
]