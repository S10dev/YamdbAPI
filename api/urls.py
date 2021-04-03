from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('titles', views.TitleViewSet)
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
