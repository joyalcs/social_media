from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('register/<int:id>/', views.UserRegisterView.as_view()),
    path('verify-otp/', views.EmailVerificationview.as_view()),
    path('send_reset_password_email/', views.UserResetPasswordEmailView.as_view()),
    path('reset_password/<int:uid>/<token>/', views.ResetPasswordView.as_view())
]
