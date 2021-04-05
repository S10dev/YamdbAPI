from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets
from django.contrib.auth.models import User
from .serializers import EmailSerializer, Confirm_RegistrationSerializer, TitleSerializer, GenreSerializer, CategorySerializer, UserSerializer
from django.core.mail import send_mail
import random
import string
from .permissions import IsModerator, IsAdmin, IsSafe, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rates.models import Title, Genre, Category
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
# Create your views here.

class PostEmail(APIView):
    # Generating random string for conf. code
    def randomStringwithDigitsAndSymbols(self, stringLength=10):
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for i in range(stringLength))


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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsSafe|IsModerator]
    pagination_class = PageNumberPagination


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


class UserViewSet(viewsets.ModelViewSet):
    lookup_field='username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination


class UserMeViewSet(APIView):
    def get(self, request):
        if request.user.username == '':
            return Response({'detail': 'Please login'})
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status= status.HTTP_200_OK)


    def patch(self, request):
        if request.user.username == '':
            return Response({'detail': 'Please login'})
        instance = request.user
        serializer = UserSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_202_ACCEPTED)