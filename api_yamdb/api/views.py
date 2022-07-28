from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.permissions import IsAdmin
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CommentSerializer,
                          ConfirmationCodeSerializer,
                          EmailSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserMeSerializer,
                          ReadOnlyTitleSerializer,
                          TitleSerializer
                          )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    if request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if User.objects.filter(email=email).exists():
            return Response(
                'Данный email уже используется!',
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif User.objects.filter(username=username).exists():
            return Response(
                'Данный никнейм уже занят. Придумайте другой!',
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user = User.objects.create(email=email, username=username)
            token = default_token_generator.make_token(user)
            resp = {'email': email, 'username': username}
            send_mail(
                subject='Код подтверждения!',
                message=str(token),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    email,
                ],
            )
        return Response(
            resp,
            status=status.HTTP_200_OK,
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not confirmation_code:
        return Response(
            'Введите код подтверждения!',
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not username:
        return Response(
            'Введите никнейм!',
            status=status.HTTP_400_BAD_REQUEST,
        )
    token_check = default_token_generator.check_token(user, confirmation_code)
    if token_check:
        refresh = RefreshToken.for_user(user)
        return Response(
            f'Ваш токен: {refresh.access_token}',
            status=status.HTTP_200_OK,
        )
    return Response(
        'Неправильный код подтверждения!',
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    """Представление для модели User.

    Набор представлений, который обеспечивает действия по умолчанию
    «получить», «обновить».
    """

    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    queryset = User.objects.all()
    search_fields = ('username',)
    ordering = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        serializer_class=UserMeSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для модели Title."""

    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для модели Review.

    Набор представлений, который обеспечивает действия по умолчанию
    «создать», «получить», «обновить», «обновить частично», «удалить».
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('-pub_date')

    def perform_create(self, serializer):
        author = self.request.user
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=author,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment.

    Набор представлений, который обеспечивает действия по умолчанию
    «создать», «получить», «обновить», «обновить частично», «удалить».
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        author = self.request.user
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=author,
            review=review
        )
