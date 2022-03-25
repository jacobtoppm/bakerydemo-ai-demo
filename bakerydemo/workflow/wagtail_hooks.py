from wagtail.core import hooks
from django.contrib.auth.models import Permission


@hooks.register("register_permissions")
def register_import_permission():
    return Permission.objects.filter(
        content_type__app_label="wagtailcore",
        codename__in=["set_assignment_size"],
    )
