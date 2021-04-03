from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class Confirm_RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=10)
from rates.models import Title, Genre, Category


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
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
    


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
