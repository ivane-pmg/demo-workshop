from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Group and Campaign URLs
    path('create_group/', views.create_group, name='create_group'),
    path('manage_groups/', views.manage_groups, name='manage_groups'),
    path('assign_campaign/<int:group_id>/', views.assign_campaign, name='assign_campaign'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('feedback/', views.feedback, name='feedback'),
    path('edit_group/<int:group_id>/', views.edit_group, name='edit_group'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
