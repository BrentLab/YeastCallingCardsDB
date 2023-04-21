from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from celery.result import AsyncResult
from callingcards.celery import app

TASK_STATE_DESCRIPTIONS = {
    'PENDING': 'The task is waiting for execution or unknown.',
    'STARTED': 'The task has been started.',
    'SUCCESS': 'The task completed successfully.',
    'FAILURE': 'The task resulted in an error.',
    'REVOKED': 'The task has been canceled by the user.',
    'RETRY': 'The task is being retried after a failure.',
}


class TaskStatusViewSet(ListModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        i = app.control.inspect()

        tasks = []
        active_tasks = i.active()
        if active_tasks:
            active_tasks = active_tasks.values()
            for worker_tasks in active_tasks:
                for task in worker_tasks:
                    task_result = AsyncResult(task['id'])
                    status = task_result.status
                    tasks.append({
                        'task_id': task['id'],
                        'endpoint': task['name'],
                        'status': status,
                        'description': TASK_STATE_DESCRIPTIONS.get(status, "Unknown")
                    })

        return Response(tasks)