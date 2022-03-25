from wagtail.admin.edit_handlers import FieldPanel
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


class FieldPanelWithFallback(FieldPanel):
    """
    A FieldPanel that falls back to rendering a template if the panel would not be shown (usually due to permissions)
    """

    def __init__(self, *args, fallback_template="", **kwargs):
        super().__init__(*args, **kwargs)
        self.fallback_template = fallback_template

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            fallback_template=self.fallback_template,
        )
        return kwargs

    def render_as_object(self):
        return (
            super().render_as_object()
            if super().is_shown()
            else mark_safe(
                render_to_string(
                    self.fallback_template,
                    {
                        "self": self,
                        "value": getattr(self.instance, self.field_name, None),
                    },
                )
            )
        )

    def render_as_field(self):
        return (
            super().render_as_field()
            if super().is_shown()
            else mark_safe(
                render_to_string(
                    self.fallback_template,
                    {
                        "self": self,
                        "value": getattr(self.instance, self.field_name, None),
                    },
                )
            )
        )

    def id_for_label(self):
        return super().id_for_label() if super().is_shown() else ""

    def is_shown(self):
        return True

    def classes(self):
        return super().classes() if super().is_shown() else []
