from django.urls import path

from . import views

app_name = 'uploader'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.registration, name='register'),
    path('register/', views.create_user, name='create_user'),
    path('upload/', views.upload_view, name='upload'),
    path('profile/success', views.handle_file_manager, name='success'),
]