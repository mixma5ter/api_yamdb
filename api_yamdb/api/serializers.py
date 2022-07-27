from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Genre, Title, Review, User


# Сериализатор модели User


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
