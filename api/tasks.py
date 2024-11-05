from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Operator
import os
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@shared_task
def generate_operator_report():
    end_time = timezone.now()
    start_time = end_time - timedelta(days=1)

    report_data = []
    for operator in Operator.objects.all():
        tagged_entries = operator.textentry_set.filter(
            tagged_at__range=(start_time, end_time)
        ).count()
        report_data.append(f"Operator {operator.user.username} tagged {tagged_entries} entries.\n")

    report_path = os.path.join('reports', f'operator_report_{end_time.date()}.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as report_file:
        report_file.writelines(report_data)

    return f"Report generated at {report_path}"


schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Generate Operator Report Daily',
    task='api.tasks.generate_operator_report',
)
