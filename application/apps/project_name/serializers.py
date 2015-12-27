from rest_framework import serializers
from . import models


URL_FIELD_NAME = 'self'


class BaseResourceModelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='uid', read_only=True)

    class Meta:
        lookup_field = "uid"
        url_field_name = "self"
        extra_kwargs = {
            URL_FIELD_NAME: {'lookup_field': 'uid'}
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        if request is not None:
            context = kwargs.pop('context', {})
            context['request'] = request
            kwargs['context'] = context
        super(BaseResourceModelSerializer, self).__init__(*args, **kwargs)


class ArticleSerializer(BaseResourceModelSerializer):
    author = serializers.HyperlinkedRelatedField(
            'user-detail', lookup_field='uid',
            queryset=models.User.objects.all(), required=False,
            allow_empty=True)
    category = serializers.HyperlinkedRelatedField(
            'category-detail', lookup_field='uid',
            queryset=models.Category.objects.all(), required=False,
            allow_empty=True)

    class Meta(BaseResourceModelSerializer.Meta):
        model = models.Article
        fields = (
            'id', 'display_name', 'slug', 'author', 'category', 'is_private',
            URL_FIELD_NAME)


class CategorySerializer(BaseResourceModelSerializer):
    class Meta(BaseResourceModelSerializer.Meta):
        model = models.Category
        fields = ('id', 'display_name', URL_FIELD_NAME)


class PublishArticleSerializer(serializers.Serializer):
    article = serializers.HyperlinkedRelatedField(
            'article-detail', lookup_field='uid',
            queryset=models.Article.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        if request is not None:
            context = kwargs.pop('context', {})
            context['request'] = request
            kwargs['context'] = context
        super(PublishArticleSerializer, self).__init__(*args, **kwargs)


class UserSerializer(BaseResourceModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta(BaseResourceModelSerializer.Meta):
        model = models.User
        fields = (
            'id', 'display_name', 'first_name', 'last_name', 'full_name',
            'email', 'is_verified_email',
            URL_FIELD_NAME)
