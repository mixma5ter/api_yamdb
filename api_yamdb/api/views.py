from rest_framework import viewsets

from .serializers import CommentSerializer, ReviewSerializer


# Представление для модели User


# Представление для модели Genre


# Представление для модели Category


# Представление для модели Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для модели Review.

    Набор представлений, который обеспечивает действия по умолчанию
    «создать», «получить», «обновить», «обновить частично», «удалить».
    """

    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment.

    Набор представлений, который обеспечивает действия по умолчанию
    «создать», «получить», «обновить», «обновить частично», «удалить».
    """

    serializer_class = CommentSerializer
