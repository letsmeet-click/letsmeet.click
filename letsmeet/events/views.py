from rules.contrib.views import PermissionRequiredMixin

from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
)

from .models import Event, EventRSVP, EventComment
from .forms import EventUpdateForm, EventCommentCreateForm


class CommunityEventMixin:
    def get_object(self, queryset=None):
        return get_object_or_404(
            Event,
            slug=self.kwargs.get('slug'),
            community__slug=self.kwargs.get('community_slug'))


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, CommunityEventMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    permission_required = 'event.can_edit'
    form_class = EventUpdateForm


class EventDetailView(CommunityEventMixin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = EventCommentCreateForm()
        return context


class EventRSVPView(LoginRequiredMixin, CommunityEventMixin, DetailView):
    model = Event
    template_name = 'events/event_rsvp.html'

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        if event.is_past():
            messages.error(request, 'You can not RSVP for past events.')
            return redirect(event)

        return super().get(request, *args, **kwargs)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if event.is_past():
            messages.error(request, 'You can not RSVP for past events.')
            return redirect(event)

        event.community.subscribe_user(request.user)
        answer = self.kwargs.get('answer')
        if answer == 'reset':
            try:
                EventRSVP.objects.get(event=event, user=request.user).delete()
            except EventRSVP.DoesNotExist:
                pass  # yes, quantifiedcode, this is intentional
        else:
            EventRSVP.objects.get_or_create(
                event=event, user=request.user,
                defaults={
                    'coming': True if answer == 'yes' else False
                }
            )

        return redirect(event)


class EventCommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CommunityEventMixin, CreateView):
    model = EventComment
    form_class = EventCommentCreateForm
    template_name = 'events/eventcomment_create.html'
    permission_required = 'event.can_create_comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_object()
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.event = self.get_object()
        comment.user = self.request.user
        comment.save()
        return redirect(comment.event)
