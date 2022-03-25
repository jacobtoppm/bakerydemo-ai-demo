from django.db import migrations
from wagtail.images import get_image_model_string


def create_assign_permission(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    page_content_type = ContentType.objects.get_by_natural_key("wagtailcore", "page")
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.get_or_create(
        codename="set_assignment_size",
        name="Can set assignment size",
        content_type=page_content_type,
    )


def delete_assign_permission(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    page_content_type = ContentType.objects.get_by_natural_key("wagtailcore", "page")
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.filter(
        codename="set_assignment_size",
        name="Can set assignment size",
        content_type=page_content_type,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0002_delete_old_workflows"),
        ("auth", "0011_update_proxy_permissions"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_assign_permission, delete_assign_permission),
    ]
