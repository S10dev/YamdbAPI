from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('titles', views.TitleViewSet)
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/email/', views.PostEmail.as_view()),
    path('auth/token/', views.Confirm_registration.as_view(), name='token_obtain'),
]