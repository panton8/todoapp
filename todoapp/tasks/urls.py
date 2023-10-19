from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('update_task/<str:pk>/', views.updateTask, name='update_task'),
    path('delete_task/<str:pk>/', views.deleteTask, name='delete_task'),
    path('complete_task/<str:pk>/', views.completeTask, name='complete_task'),
    path('day/', views.current_day_tasks, name='list_by_day')
]