from wagtail.admin.forms.pages import WagtailAdminPageForm
from django.core.exceptions import ValidationError


class FormWithAssignment(WagtailAdminPageForm):
    """
    Base form class for AssignablePage subclasses
    """

    assignment_field_name = "assignment_size"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment_field = self.fields.get(self.assignment_field_name)
        if self.assignment_field:
            # We need to make sure that the size choices available are the ones assigned to the workflow this page will get
            from .models import AssignmentSizeChoice

            closest_created_page = (
                self.instance if self.instance.pk else self.parent_page
            )
            self.assignment_field.queryset = AssignmentSizeChoice.objects.filter(
                group__workflows__workflow_ptr=closest_created_page.get_workflow().pk
            )

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.workflow_in_progress or self.data.get("action-submit"):
            assignment_size = (
                cleaned_data.get(self.assignment_field_name)
                if self.assignment_field
                else self.instance.assignment_size
            )
            if not assignment_size:
                error = ValidationError(
                    "Assignment size must be set for a page to be moderated"
                )
                if self.assignment_field:
                    self.add_error(self.assignment_field_name, error)
                else:
                    raise error
        return cleaned_data
