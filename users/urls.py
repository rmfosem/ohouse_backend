from django.urls import path
from .views import EmailVerificationView, VerifyCodeView, RegisterView

urlpatterns = [
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('register/', RegisterView.as_view(), name='register'),
]