from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet,
                    ReviewViewSet,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    UserViewSet,
                    TokenObtainView,
                    register_user)

router_v1 = DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(r'categories', CategoryViewSet, basename="categories")
router_v1.register(r'genres', GenreViewSet, basename="genres")
router_v1.register(r'titles', TitleViewSet, basename="titles")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path("v1/auth/signup/", register_user, name='registration'),
    path("v1/auth/token/", TokenObtainView.as_view(),
        name='token_obtain_pair',),
]
