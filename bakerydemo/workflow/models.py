from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from wagtail.core.models import Page, Workflow
from wagtail.core.fields import RichTextField
from .forms import FormWithAssignment
from .edit_handlers import FieldPanelWithFallback


@register_snippet
class AssignmentSizeChoiceGroup(ClusterableModel):
    name = models.CharField(max_length=255)

    panels = [FieldPanel("name"), InlinePanel("choices", min_num=1, heading="Choices")]

    def __str__(self):
        return self.name


class AssignmentSizeChoice(models.Model):
    group = ParentalKey(
        AssignmentSizeChoiceGroup, on_delete=models.CASCADE, related_name="choices"
    )
    label = models.CharField(max_length=255, blank=False)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.label


class AssignablePage(Page):
    """
    Base page class for Pages that track an assignment size,
    """

    assignment_size = models.ForeignKey(
        AssignmentSizeChoice, on_delete=models.PROTECT, null=True, blank=True
    )

    settings_panels = [
        MultiFieldPanel(
            [
                FieldPanelWithFallback(
                    "assignment_size",
                    permission="wagtailcore.set_assignment_size",
                    fallback_template="workflow/assignment_fallback.html",
                )
            ],
            heading="Assignment",
        )
    ] + Page.settings_panels

    base_form_class = FormWithAssignment

    class Meta:
        abstract = True


class CustomWorkflow(Workflow):
    assignment_size_choices = models.ForeignKey(
        AssignmentSizeChoiceGroup, on_delete=models.PROTECT, related_name="workflows"
    )


class TestPage(AssignablePage):
    intro = RichTextField(blank=True)

    content_panels = AssignablePage.content_panels + [FieldPanel("intro")]
