from django.urls import path
from project_manager import views as pm_view

urlpatterns = [
    path('', pm_view.index, name='dashboard'),
  # path('book/<int:id>', pm_view.book, name='book'),
  # path('return_doc/<int:id>', pm_view.return_doc, name='return_doc'),
]
