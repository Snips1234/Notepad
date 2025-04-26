from django.urls import path
from . import views
from .views import delete_image

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('delete-image/<int:image_id>/', delete_image, name='delete_image'),
]
