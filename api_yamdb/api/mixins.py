from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet,
                               mixins.ListModelMixin,):
    """Mixin обрабатывает создание, удаление и получение списка объектов."""

    pass
