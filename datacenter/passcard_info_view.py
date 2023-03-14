from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datacenter.models import get_duration, format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits_all = Visit.objects.filter(passcard=passcard)
    passcard_visits = []
    for visit in visits_all:
        entered_at = visit.entered_at
        duration = get_duration(visit)
        time_duration = format_duration(duration)


        this_passcard_visits = {
                'entered_at': entered_at,
                'duration': time_duration,
                'is_strange': is_visit_long(visit, minutes=60)
            }

        passcard_visits.append(this_passcard_visits)
    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits
    }
    return render(request, 'passcard_info.html', context)
