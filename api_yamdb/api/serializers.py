from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Title, Review, User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя создавать пользователя с ником "me"!'
            )
        return value


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена."""

    username_field = User.USERNAME_FIELD
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        current_user = get_object_or_404(
            User, username=attrs[self.username_field]
        )
        token = attrs['confirmation_code']
        if not default_token_generator.check_token(current_user, token):
            raise serializers.ValidationError(
                'Неправильный код подтверждения!'
            )
        token = AccessToken.get_token(current_user)
        return {'token': str(token)}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Создать пользователя me нельзя'
            )
        return value


class UserMeSerializer(UserSerializer):
    """Сериализатор модели User c ограничением смены роли."""

    class Meta:
        fields = (
            'username',
            'bio',
            'email',
            'first_name',
            'last_name',
            'role',
        )
        read_only_fields = ['role']
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""

    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )
        model = Title

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return None
        return round(rating, 1)



class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для созания объекта."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        queryset = self.context.get('view').get_queryset()
        if request.method == 'PATCH':
            return data
        if queryset.filter(author=request.user).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять больше 1 отзыва на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
