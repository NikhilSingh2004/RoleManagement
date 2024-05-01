from django.urls import path
from . import views

urlpatterns = [
    # path('users/login/', views.login, name='login'),
    # path('users/logout/', views.logout, name='logout'),
    path('users/create/', views.create_user, name='create-user'),
    path('users/<int:pk>/update/', views.update_user, name='update-user'),
    path('users/<int:pk>/disable/', views.disable_user, name='disable-user'),
    path('roles/create/', views.create_role, name='create-role'),
    path('roles/<int:pk>/update/', views.update_role, name='update-role'),
    path('roles/<int:pk>/delete/', views.delete_role, name='delete-role'),
]
