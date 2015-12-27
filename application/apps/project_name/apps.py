from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = __name__.split('.')[0]
    verbose_name = _('{{ project_name }}')

    def ready(self):
        from . import signals
