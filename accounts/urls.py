from django.urls import path
from .views import SignupView, SigninView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', SigninView.as_view(), name='login'),
]
