from wagtail.workflows import publish_workflow_state
from django.db import transaction


@transaction.atomic
def pay_author_and_publish(workflow_state, *args, **kwargs):
    page = workflow_state.page.specific.get_latest_revision().as_page_object()
    current_assignment_size = page.assignment_size
    page.assignment_size = None
    page.save_revision()
    publish_workflow_state(workflow_state)
    print(f"we would pay {workflow_state.requested_by} here, then send them an email")
