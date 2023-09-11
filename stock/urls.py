from django.urls import path
from django.urls.conf import re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='stock-home'),

    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('bills/', views.BillListView.as_view(), name='bills'),

    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('bill/<uuid:pk>/', views.BillDetailView.as_view(), name='bill-detail'),

    path('category/<int:pk>/edit/', views.CategoryEditView.as_view(), name='category-edit'),
    path('product/<int:pk>/edit/', views.ProductEditView.as_view(), name='product-edit'),
    path('product/<int:pk>/stock/edit/', views.ProductStockEditView.as_view(), name='product-stock-edit'),

    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    path('category/new/', views.NewCategoryView.as_view(), name='new-category'),
    path('product/new/', views.NewProductView.as_view(), name='new-product'),
]