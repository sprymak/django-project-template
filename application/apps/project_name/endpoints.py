"""This is where the Web API endpoints, such as REST or RPC, are defined. """
import logging
from django.utils import six
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.routers import DynamicDetailRoute, \
    DynamicListRoute, Route, SimpleRouter

from . import base
from . import models
from . import serializers

logger = logging.getLogger(__name__)


def IsOwner(field_name):
    class Permission(permissions.IsAuthenticated):
        def __init__(self):
            self.field_name = field_name
            super(Permission, self).__init__()

        def has_object_permission(self, request, view, obj):
            owner = getattr(obj, self.field_name, None)
            user = request.user
            if isinstance(owner, six.integer_types):
                user = user.pk
            return owner is not None and owner == user


    return Permission


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
        )


class Router(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/id/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{methodname}/{lookup}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]


class BaseViewSet(viewsets.GenericViewSet):
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    permission_classes = [permissions.DjangoModelPermissions]

    def get_many(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        if kwargs:
            queryset = queryset.filter(*args, **kwargs)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_single(self, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), *args, **kwargs)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ActionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @list_route(methods=['POST'])
    def publish(self, request):
        kwargs = dict(data=request.data, request=request)
        serializer = serializers.PublishArticleSerializer(**kwargs)
        serializer.is_valid(raise_exception=True)
        article = serializer.validated_data['article']

        if article.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        base.publish_article(article)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(RetrieveModelMixin, ListModelMixin, BaseViewSet):
    permission_classes = [IsOwner('author')]
    queryset = models.Article.objects.none()
    serializer_class = serializers.ArticleSerializer

    def get_queryset(self):
        return self.request.user.articles.public()

    @list_route(methods=['GET'])
    def mine(self, request):
        return self.get_many(
                queryset=self.request.user.articles.all(),
                author=self.request.user)


class CategoryViewSet(RetrieveModelMixin, ListModelMixin, BaseViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, BaseViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.User.objects.none()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.User.objects.all()
        return models.User.objects.filter(pk=self.request.user.pk)

    @list_route()
    def active(self, request):
        return self.get_many(is_active=True)

    @list_route(methods=['GET', 'PUT'])
    def me(self, request):
        return self.get_single(pk=request.user.pk)

    @list_route()
    def staff(self, request):
        return self.get_many(is_staff=True)

    @detail_route()
    def username(self, request, uid=None):
        return self.get_single(username=uid)


router = Router(trailing_slash=False)
router.register(r'actions', ActionViewSet, base_name='action')
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
