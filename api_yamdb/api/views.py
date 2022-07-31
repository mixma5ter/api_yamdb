from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaff
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          CreateUserSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleCreateSerializer,
                          TitleSerializer,
                          TokenObtainSerializer,
                          UserSerializer,
                          UserMeSerializer,
                          )


def send_registration_mail(user, token):
    send_mail(
        subject='Регистрация на YaMDb',
        message=(
            f'{user.username}, ваш код подтверждения для получения токена: '
            f'{token}'
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


@api_view(['POST'])
def register_user(request):
    """Регистрация нового пользователя."""

    serializer = CreateUserSerializer(data=request.data)
    try:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email'],
        )
    except Exception:
        user = None
    if not user:
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    token = default_token_generator.make_token(user)
    send_registration_mail(user, token)
    return Response(request.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenObtainPairView):
    """Получения токена."""

    serializer_class = TokenObtainSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Представление для модели User."""

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
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для модели Title."""

    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaff,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaff,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_id,
        )
        return review.comments.filter(review__title_id=title_id).order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_id,
        )
        serializer.save(author=self.request.user, review=review)
