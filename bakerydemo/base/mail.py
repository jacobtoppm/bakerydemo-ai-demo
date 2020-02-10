from django.template.loader import render_to_string

from wagtail.admin.mail import Notifier
from wagtail.core.models import WorkflowState, TaskState

import requests
import json


class SlackIntegrationNotifier(Notifier):
    def get_valid_recipients(self, instance, **kwargs):
        return {'https://hooks.slack.com/services/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'}

    def get_template_base_prefix(self, instance, **kwargs):
        return super().get_template_base_prefix(instance, **kwargs)+'slack_'

    def send_notifications(self, template_set, context, recipients, **kwargs):
        message_content = json.dumps(json.loads(render_to_string(template_set['text'], context).strip()))
        sent_count = 0
        for recipient in recipients:
            response = requests.post(recipient, message_content, json=True)
            if response.status_code==200:
                sent_count += 1
        if sent_count == len(recipients):
            return True
        return False


class WorkflowSlackNotifier(SlackIntegrationNotifier):
    def __init__(self):
        super().__init__((WorkflowState,))

    def get_context(self, workflow_state, **kwargs):
        context = super().get_context(workflow_state, **kwargs)
        context['page'] = workflow_state.page
        context['workflow'] = workflow_state.workflow
        return context


class WorkflowSubmissionSlackNotifier(WorkflowSlackNotifier):

    notification = 'submitted'


class TaskSlackNotifier(SlackIntegrationNotifier):
    def __init__(self):
        super().__init__((TaskState,))

    def get_context(self, task_state, **kwargs):
        context = super().get_context(task_state, **kwargs)
        context['page'] = task_state.workflow_state.page
        context['task'] = task_state.task.specific
        return context


class TaskSubmissionSlackNotifier(TaskSlackNotifier):

    notification = 'submitted'

