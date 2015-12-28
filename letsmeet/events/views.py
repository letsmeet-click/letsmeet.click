from rules.contrib.views import PermissionRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
)

from .models import Event, EventRSVP


class EventListView(ListView):
    model = Event


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'slug', 'begin', 'end']
    template_name = 'events/event_update.html'
    permission_required = 'event.can_edit'


class EventDetailView(DetailView):
    model = Event


class EventRSVPView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_rsvp.html'
    permission_required = 'event.can_rsvp'

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        answer = self.kwargs.get('answer')
        if answer == 'reset':
            try:
                EventRSVP.objects.get(event=event, user=request.user).delete()
            except EventRSVP.DoesNotExist:
                pass
        else:
            EventRSVP.objects.get_or_create(
                event=event, user=request.user,
                defaults={
                    'coming': True if answer == 'yes' else False
                }
            )

        return redirect(event)
