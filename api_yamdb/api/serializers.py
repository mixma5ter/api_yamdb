from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Title, Review, User


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


# Сериализатор модели Genre


# Сериализатор модели Category


# Сериализатор модели Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    class Meta:
        model = Comment
        fields = '__all__'
