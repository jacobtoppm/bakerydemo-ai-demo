from .mail import TaskSubmissionSlackNotifier, WorkflowSubmissionSlackNotifier
from wagtail.core.models import TaskState, WorkflowState
from wagtail.core.signals import task_submitted, workflow_approved, workflow_rejected, workflow_submitted


workflow_submission_slack_notifier = WorkflowSubmissionSlackNotifier()
task_submission_slack_notifier = TaskSubmissionSlackNotifier()


def register_signal_handlers():
    workflow_submitted.connect(workflow_submission_slack_notifier, sender=WorkflowState, dispatch_uid='workflow_state_submitted_slack_notification')
    task_submitted.connect(task_submission_slack_notifier, sender=TaskState,
                               dispatch_uid='task_state_submitted_slack_notification')

