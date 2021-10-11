import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rates.models import Title, Genre, Category, Review, Comment
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg
import django_filters.rest_framework
from .serializers import (
    EmailSerializer, Confirm_RegistrationSerializer, TitleSerializer,
    GenreSerializer, CategorySerializer, UserSerializer,
    ReviewSerializer, CommentSerializer, UserMeSerializer
    )
from .permissions import IsModerator, IsAdmin, IsPostMethod, IsSafe, IsOwner
User = get_user_model()


class PostEmail(APIView):
    def randomStringwithDigitsAndSymbols(self, stringLength=10):
        '''Generating random string for the account verification'''
        rand_chars = string.ascii_letters + string.digits
        return \
            ''.join(random.choice(rand_chars) for _ in range(stringLength))

    def post(self, request):
        '''Getting an email from user.
        After validation sending him a confirmation_code'''
        serializer = EmailSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        confirmation_code = f'{self.randomStringwithDigitsAndSymbols()}'
        email = f'{serializer.validated_data["email"]}'

        if User.objects.all().filter(email=email):
            return Response({'error': 'email already registered'})

        send_mail(
            'Validation code for JWT token',
            confirmation_code,
            'senddjango2@gmail.com',
            [serializer.validated_data["email"]],
            fail_silently=False
            )

        try:
            User.objects.create(
                username=f'user{User.objects.all().count()+1}',
                email=email,
                confirmation_code=confirmation_code
                )
        except Exception as e:
            return Response(
                {'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class Confirm_registration(APIView):
    '''Getting an email and a confirmation_code form user.
    Then comparing it with value frin DB.
    If success sending JWT token to user'''
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'token': str(refresh.access_token),
        }

    def post(self, request):
        serializer = Confirm_RegistrationSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        email = serializer.validated_data["email"]
        confirmation_code = serializer.validated_data['confirmation_code']

        try:
            user = User.objects.get(email=f'{email}')
        except Exception:
            return Response(
                {'email': f'{email}'}, status=status.HTTP_400_BAD_REQUEST)

        if user.confirmation_code == confirmation_code:
            return Response(
                self.get_token_for_user(user), status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'confirmation_code': f'{confirmation_code}'},
                status=status.HTTP_400_BAD_REQUEST
                )


class TitleViewSet(viewsets.ModelViewSet):
    '''Viewset for titles'''
    serializer_class = TitleSerializer
    permission_classes = [IsSafe | IsModerator]
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
    '''Viewset for genres'''
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsSafe | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class CategoryViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
        ):
    '''Viewset for categories'''
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSafe | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class UserViewSet(viewsets.ModelViewSet):
    '''Viewset for entire users (only admin access)'''
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]


class UserMeViewSet(APIView):
    '''Viewset for one user (only Authenticated user access)'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        instance = request.user
        serializer = UserMeSerializer(
            instance=instance, data=request.data, partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ReviewViewSet(viewsets.ModelViewSet):
    '''Viewset for reviews'''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsSafe | (IsAuthenticated & IsPostMethod) |
        IsAdmin | IsOwner | IsModerator
        ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        queryset = self.queryset.filter(title__id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user, title=Title.objects.get(id=title_id)
            )


class CommentViewSet(viewsets.ModelViewSet):
    '''Viewset for comments'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsSafe | (IsAuthenticated & IsPostMethod) |
        IsAdmin | IsOwner | IsModerator
        ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = self.queryset.filter
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, id=title_id)
        get_object_or_404(Review, id=review_id)
        queryset = self.queryset.filter(review__id=review_id)
        return queryset


def redirect_to_index_API(request):
    '''Redirect from localhost to localhost/api/v1/'''
    return redirect('api/v1/')
