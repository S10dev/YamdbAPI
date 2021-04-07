from rest_framework import serializers
from django.contrib.auth.models import User
from rates.models import Title, Genre, Category, Review, Comment

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class Confirm_RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=10)


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug
        }


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug
        }



class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(slug_field='slug', queryset=Genre.objects.all(), required=False)
    category = CategoryField(slug_field='slug', queryset=Category.objects.all(), required=False)
    rating = serializers.IntegerField()
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
    


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "bio", "email", "role")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Review
        exclude = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
