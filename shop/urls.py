from django.urls import path
from . import views

urlpatterns = [
    # Home view of shop
    path('', views.HomeView.as_view(), name='shop-home'),
    # Cart view for adding products
    path('cart/', views.CartView.as_view(), name='cart'),
    # Checkout request containing products, quantity info; returns json response
    path('checkout/', views.checkout_response),
    # Temporary memo, details view after successful checkout
    path('checkout/<uuid:pk>/', views.CheckoutDetailView.as_view(), name='checkout-detail'),
    # Staff list, management
    path('staffs/', views.StaffListView.as_view(), name='staffs'),
    # Staff detail
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff-detail'),
    # Staff edit
    path('staff/<int:pk>/edit/', views.StaffEditView.as_view(), name='staff-edit'),
    # Staff credential edit
    path('staff/<int:pk>credential-edit/', views.StaffCredentialEditView.as_view(), name='staff-credential-edit'),
    # Staff delete
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff-delete'),
    # New Staff
    path('staff/new/', views.NewStaffView.as_view(), name='new-staff'),
    # Account detail
    path('account/', views.AccountDetailView.as_view(), name='account-detail'),
    # Account edit
    path('account/edit/', views.AcocuntEditView.as_view(), name='account-edit'),
    # Account credential edit
    path('account/credential-edit/', views.AccountCredentialEditView.as_view(), name='account-credential-edit'),
]