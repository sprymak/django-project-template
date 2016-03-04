from django.conf.urls import include, url
from django.contrib.auth import REDIRECT_FIELD_NAME
from . import endpoints
from . import views


urlpatterns = [
    url(r'^api/', include(endpoints.router.urls)),
    url(r'^$', views.article_list, name='{{ project_name }}-article-list'),
    url(r'^add$', views.add_article, name='{{ project_name }}-article-add'),
    url(r'^(?P<slug>[\w-]+)$', views.article_detail,
        name='{{ project_name }}-article-detail'),
    url(r'^(?P<pk>\d+)/change$', views.change_article,
        name='{{ project_name }}-article-change'),
    url(r'^(?P<pk>\d+)/change\?%s=(?P<next_page>.*)$' % REDIRECT_FIELD_NAME,
        views.change_article, name='{{ project_name }}-article-change-next'),
    url(r'^(?P<pk>\d+)/delete', views.delete_article,
        name='{{ project_name }}-article-delete'),
    url(r'^(?P<pk>\d+)/delete\?%s=(?P<next_page>.*)$' % REDIRECT_FIELD_NAME,
        views.delete_article, name='{{ project_name }}-article-delete-next'),
]
