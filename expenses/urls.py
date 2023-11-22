from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<id>', views.delete_expense, name='delete-expense'),
]