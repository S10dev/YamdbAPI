from django.shortcuts import render
from rest_framework import viewsets
from rates.models import Title, Genre, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = []
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    pagination_class = PageNumberPagination