from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import (
    EmailSerializer, Confirm_RegistrationSerializer, TitleSerializer,
    GenreSerializer, CategorySerializer, UserSerializer,
    ReviewSerializer, CommentSerializer
    )
from django.core.mail import send_mail
import random
import string
from .permissions import IsModerator, IsAdmin, IsSafe, IsOwner, IsPost
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rates.models import Title, Genre, Category, Review, Comment
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from django.db.models import Avg, Max, Min
import django_filters.rest_framework
# Create your views here.

class PostEmail(APIView):
    def randomStringwithDigitsAndSymbols(self, stringLength=10):
        '''Generating random string for the account verification'''
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for _ in range(stringLength))


    def post(self, request):
        serializer = EmailSerializer(data = request.POST)
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        confirmation_code = f'{self.randomStringwithDigitsAndSymbols()}'
        email = f'{serializer.validated_data["email"]}'

        if User.objects.all().filter(email=email):
            return Response({'error': 'email already registered'})

        try:
            User.objects.create(
                username = f'user{User.objects.all().count()+1}',
                email = email,
                confirmation_code = confirmation_code
                )
        except Exception as e:
            return Response({'error': f'{e}'} , status = status.HTTP_400_BAD_REQUEST)

        send_mail(
            'Validation code for JWT token',
            confirmation_code,
            'senddjango2@gmail.com',
            [serializer.validated_data["email"]],
            fail_silently=False
            )

        return Response(serializer.data , status = status.HTTP_202_ACCEPTED)


class Confirm_registration(APIView):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'token': str(refresh.access_token),
        }


    def post(self, request):
        serializer = Confirm_RegistrationSerializer(data = request.POST)
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data["email"]
        confirmation_code = serializer.validated_data['confirmation_code']

        try:
            user = User.objects.get(email = f'{email}')
        except Exception:
            return Response({'email': f'{email}'}, status = status.HTTP_400_BAD_REQUEST)

        if user.confirmation_code == confirmation_code:
            return Response(self.get_tokens_for_user(user), status = status.HTTP_200_OK)
        else:
            return Response({'confirmation_code': f'{confirmation_code}'}, status = status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [IsSafe|IsModerator]
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category', 'name', 'year']


    def get_queryset(self):
        queryset = Title.objects.all().annotate(rating=Avg('review__score'))
        return queryset


class GenreViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    lookup_field='slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsSafe|IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name',]


class CategoryViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    lookup_field='slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSafe|IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name',]


class UserViewSet(viewsets.ModelViewSet):
    lookup_field='username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username',]


class UserMeViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status= status.HTTP_200_OK)


    def patch(self, request):
        instance = request.user
        serializer = UserSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_202_ACCEPTED)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsSafe|(IsAuthenticated&IsPost)|IsAdmin|IsOwner|IsModerator]
    pagination_class = PageNumberPagination


    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id = title_id)
        queryset = self.queryset.filter(title__id = title_id)
        return queryset

    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title=Title.objects.get(id=title_id))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsSafe|(IsAuthenticated&IsPost)|IsAdmin|IsOwner|IsModerator]
    pagination_class = PageNumberPagination


    def get_queryset(self):
        queryset = self.queryset.filter
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, id = title_id)
        get_object_or_404(Review, id = review_id)
        queryset = self.queryset.filter(review__id=review_id)
        return queryset