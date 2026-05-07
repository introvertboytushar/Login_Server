from django.urls import path
from .views import RegisterView, LoginView, VerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', VerifyView.as_view(), name='verify'),
]
