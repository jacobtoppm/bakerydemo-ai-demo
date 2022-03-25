from django.db import migrations


def delete_unextended_workflows(apps, schema_editor):
    Workflow = apps.get_model("wagtailcore", "Workflow")
    db_alias = schema_editor.connection.alias
    Workflow.objects.using(db_alias).filter(customworkflow__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(delete_unextended_workflows),
    ]
