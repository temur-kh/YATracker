from django.urls import path
from user_manager import views

urlpatterns = [
    path('', views.personal, name='personal'),
]
