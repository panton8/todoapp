from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task'),
    path('complete_task/<str:pk>/', views.complete_task, name='complete_task'),
    path('day/', views.current_day_tasks, name='list_by_day'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
    path('signup/', views.sign_up, name='sign_up'),
]
