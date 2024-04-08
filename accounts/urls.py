from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile', views.GetUserProfile.as_view(), name='get_profile'),
    path('profile/<profile_type>', views.SwitchUserProfile.as_view(), name='switch_profile'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('set_password/<str:token>',
         views.set_password.as_view(), name='set_password'),
    path('reset_password/<str:token>',
         views.reset_password.as_view(), name='reset_password'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('users/<str:uuid>/update/profile',
         views.UpdateProfile.as_view(), name='update_profile'),
     path('verify_email/<str:token>',
         views.verify_email.as_view(), name='verify_email'),
     path('resend/verify_email/', views.ResendVerificationEmail.as_view(), name='resend_verification_email'),
]
