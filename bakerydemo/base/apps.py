from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BakerydemoBaseAppConfig(AppConfig):
    name = 'bakerydemo.base'
    label = 'base'
    verbose_name = _("Bakerydemo base")

    def ready(self):
        from .signal_handlers import register_signal_handlers
        register_signal_handlers()
