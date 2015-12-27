from __future__ import unicode_literals
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from mcutils.http import build_absolute_uri


class TimeStampedModelMixin(models.Model):
    date_created = models.DateTimeField(
            auto_now_add=True, verbose_name=_('created'))
    date_updated = models.DateTimeField(
            auto_now=True, null=True, verbose_name=_('updated'))

    class Meta:
        abstract = True


class BaseManager(models.Manager):
    """ Base objects manager for models with natural keys. """

    def get_by_natural_key(self, uid):
        return self.get(uid=uid)


class ArticleQuerySet(models.QuerySet):
    def private(self):
        return self.filter(is_private=True)

    def public(self):
        return self.filter(is_private=False)


class ArticleManager(models.Manager):
    def foo(self):
        return


@python_2_unicode_compatible
class Article(TimeStampedModelMixin, models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles')
    is_private = models.BooleanField(default=True, verbose_name=_('private'))
    category = models.ForeignKey(
        'Category', null=True, blank=True, related_name='articles',
        verbose_name=_('category'))

    objects = ArticleManager.from_queryset(ArticleQuerySet)()

    class Meta:
        permissions = (
            # extend default ['add_*', 'change_*', 'delete_*'] permissions
            ('index_article', _('Can index article')),
            ('get_article', _('Can get article')),
        )
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = '-date_created',

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Note: 'http://localhost' will be used as base URL if the app
        # is running from shell and WSGI environment is not available.
        return build_absolute_uri(reverse('article-detail', args=[self.uid]))

    def natural_key(self):
        return self.uid,

    @property
    def display_name(self):
        return self.title


@python_2_unicode_compatible
class Category(TimeStampedModelMixin, models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    display_name = models.CharField(blank=True, default='', max_length=150)


    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = 'display_name',


    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        # Note: 'http://localhost' will be used as base URL if the app
        # is running from shell and WSGI environment is not available.
        return build_absolute_uri(reverse('category-detail', args=[self.uid]))

    def natural_key(self):
        return self.uid,


@python_2_unicode_compatible
class User(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    is_verified_email = models.BooleanField(_('verified'), default=False)
    date_updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name=_("updated"))
    expiration_date = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(
        blank=True, null=True, verbose_name=_('last seen'))
    first_ip_addr = models.GenericIPAddressField(
        blank=True, null=True, verbose_name=_('first IP address'))
    last_ip_addr = models.GenericIPAddressField(
        blank=True, null=True, verbose_name=_('last IP address'))
    timezone = TimeZoneField(default='UTC')

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        # Note: 'http://localhost' will be used as base URL if the app
        # is running from shell and WSGI environment is not available.
        return build_absolute_uri(reverse('user-detail', args=[self.uid]))

    def natural_key(self):
        return self.uid,

    @property
    def display_name(self):
        full_name = self.get_full_name() or self.get_username()
        if not full_name:
            full_name = self.email or self.uid
        return six.text_type(full_name)

    def is_expired(self):
        if not self.expiration_date:
            return False
        return self.expiration_date <= timezone.now()

    is_expired.boolean = True
