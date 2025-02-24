from django.urls import path
from .views import (
    index, RefreshTokenView, LoginView, RegisterUserView, UserDetailView,
    FamilyGroupListView, UserGroupPermissionsView, AssetListView, AssetDetailView,
    DashboardView, TransactionListView, DocumentListView, DocumentDetailView,
    NotificationListView, NotificationUpdateView, BudgetInsightView, TrendInsightView
)

urlpatterns = [
    # General index route (optional, remove if not needed)
    path('', index, name='index'),
    
    # Authentication routes
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='refresh_token'),
    
    # User management routes
    path('users/', RegisterUserView.as_view(), name='register_user'),
    path('users/<uuid:id>/', UserDetailView.as_view(), name='user_detail'),
    
    # Family group routes
    path('groups/', FamilyGroupListView.as_view(), name='group_list'),
    path('groups/<uuid:group_id>/permissions/', UserGroupPermissionsView.as_view(), name='group_permissions'),
    
    # Asset routes
    path('assets/', AssetListView.as_view(), name='asset_list'),
    path('assets/<uuid:id>/', AssetDetailView.as_view(), name='asset_detail'),
    
    # Dashboard route
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Transaction routes
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    
    # Document routes
    path('documents/', DocumentListView.as_view(), name='document_list'),
    path('documents/<uuid:id>/', DocumentDetailView.as_view(), name='document_detail'),
    
    # Notification routes
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<uuid:id>/', NotificationUpdateView.as_view(), name='notification_update'),
    
    # AI-driven insight routes
    path('insights/budget/', BudgetInsightView.as_view(), name='budget_insight'),
    path('insights/trends/', TrendInsightView.as_view(), name='trend_insight'),
]