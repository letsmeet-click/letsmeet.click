from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
)

from .models import Event


class EventListView(ListView):
    model = Event


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'slug', 'begin', 'end']
    template_name = 'events/event_update.html'


class EventDetailView(DetailView):
    model = Event


class EventRSVPView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_rsvp.html'

    def post(self, request, *args, **kwargs):
        return redirect(self.get_object())
