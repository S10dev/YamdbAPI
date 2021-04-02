from django.urls import path, include
from . import views


urlpatterns = [
    path('test/', views.T.as_view()),
    path('auth/email/', views.PostEmail.as_view()),
    path('auth/token/', views.Confirm_registration.as_view(), name='token_obtain'),
]
