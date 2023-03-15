from django.db import models
import django
from django.utils import timezone
import time
from datetime import datetime
class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
def get_duration(visit):
    entered_at = visit.entered_at
    leaved_at = django.utils.timezone.localtime(visit.leaved_at)
    duration = leaved_at - entered_at
    return duration


def format_duration(duration):
    all_time_duration_seconds = duration.total_seconds()
    time_duration_hours = int(all_time_duration_seconds // 3600)
    time_duration_minutes = int((all_time_duration_seconds % 3600) // 60)
    all_time_duration = f'{time_duration_hours}:{time_duration_minutes}'
    time_duration = datetime.strptime(all_time_duration, "%H:%M")

    return time_duration.time()

def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    duration_minutes = duration.total_seconds() / 60
    return duration_minutes > minutes
