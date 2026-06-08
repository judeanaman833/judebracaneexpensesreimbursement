from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('add/', ExpenseCreateView.as_view(), name='expense-add'),
    path('<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-edit'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    path('export/pdf/', export_expenses_pdf, name='export-expenses-pdf'),
    path('export/csv/', export_expenses_csv, name='export-expenses-csv'),
]
