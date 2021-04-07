from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('titles', views.TitleViewSet, 'Title')
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)
router.register('users', views.UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet
    )

urlpatterns = [
    path('users/me', views.UserMeViewSet.as_view()),
    path('genres/<slug:slug>', views.GenreViewSet.as_view({'delete': 'destroy'})),
    path('categories/<slug:slug>', views.CategoryViewSet.as_view({'delete': 'destroy'})),
    path('', include(router.urls)),
    path('auth/email/', views.PostEmail.as_view()),
    path('auth/token/', views.Confirm_registration.as_view(), name='token_obtain'),
]