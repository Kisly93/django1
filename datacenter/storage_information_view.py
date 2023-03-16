from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in active_visits:
        who_entered = visit.passcard
        entered_at = visit.entered_at
        duration = get_duration(visit)
        time_duration = format_duration(duration)
        non_closed_visit = {
            'who_entered': who_entered,
            'entered_at': entered_at,
            'duration': time_duration,
        }

        non_closed_visits.append(non_closed_visit)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
