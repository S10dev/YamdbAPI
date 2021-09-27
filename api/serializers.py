from rest_framework import serializers
from rates.models import User
from rates.models import Title, Genre, Category, Review, Comment


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class Confirm_RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=10)


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all(), required=False
        )
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'year', 'name', 'rating', 'description', 'genre', 'category'
        )

    def get_genre(self, obj):
        return {
            'name': obj.title.all()[0].genre.name,
            'slug': obj.title.all()[0].genre.slug
            }


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
        fields = (
            "first_name", "last_name", "username", "bio", "email", "role"
            )


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
