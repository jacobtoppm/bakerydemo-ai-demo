from wagtail.admin.views.workflows import Create, Edit
from wagtail.admin.forms.workflows import get_workflow_edit_handler
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from .models import CustomWorkflow


class CustomCreate(Create):
    model = CustomWorkflow

    def get_edit_handler(self):
        if not self.edit_handler:
            edit_handler = get_workflow_edit_handler()
            edit_handler.children.append(
                FieldPanel("assignment_size_choices", heading="Choose assignment sizes")
            )
            self.edit_handler = edit_handler.bind_to(
                model=self.model, request=self.request
            )
        return self.edit_handler


class CustomEdit(Edit):
    model = CustomWorkflow

    def get_edit_handler(self):
        if not self.edit_handler:
            edit_handler = get_workflow_edit_handler()
            edit_handler.children.append(
                FieldPanel("assignment_size_choices", heading="Choose assignment sizes")
            )
            self.edit_handler = edit_handler.bind_to(
                model=self.model, request=self.request
            )
        return self.edit_handler

    def get_context_data(self):
        context = super().get_context_data()
        context["workflow"] = context["object"]
        return context
