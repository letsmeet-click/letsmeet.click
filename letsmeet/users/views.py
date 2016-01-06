import rules
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404
from django.shortcuts import redirect
from django.utils.http import urlquote
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from social.apps.django_app.default.models import UserSocialAuth
from rules.contrib.views import PermissionRequiredMixin

from .models import UserProfile


class UserProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    model = UserProfile
    permission_required = 'userprofile.can_change'
    fields = ['avatar',]

    def get_object(self):
        up, created = UserProfile.objects.get_or_create(user=self.request.user)
        return up

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(next=urlquote(reverse("profile")))
        return ctx


@rules.predicate
def can_change_userprofile(user, userprofile):
    print(user, userprofile)
    if not user or not userprofile:
        return False

    return userprofile.user == user


rules.add_perm('userprofile.can_change', can_change_userprofile)


class UserSocialAuthChangeView(LoginRequiredMixin, DetailView):
    model = UserSocialAuth
    allowed_methods = ['post']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get('id')
        if not pk:
            raise AttributeError("Post parameter 'id' is required.")
        try:
            obj = queryset.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404("No UserSocialAuth found matching the query") from None

        return obj

    def post(self, request, *args, **kwargs):
        user_social_auth = self.get_object()
        if not rules.test_rule('can_delete_user_social_auth', request.user, user_social_auth):
            messages.error(request, "Can not remove the last social account unless a password has been set.")
            return redirect('profile')
        assert isinstance(user_social_auth, UserSocialAuth)
        user_social_auth.delete()
        return redirect('profile')


class UserSocialAuthChangeView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = UserSocialAuth
    permission_required = 'userprofile.can_change'
    model = UserProfile

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        action = self.request.POST.get('action')
        if not action:
            raise AttributeError("Post parameter 'action' is required.")

        notification_type = self.request.POST.get('type')
        if not action:
            raise AttributeError("Post parameter 'type' is required.")

        if action == 'enable':
            target_value = True
        elif action == 'disable':
            target_value = False
        else:
            raise AttributeError("Invalid 'action' provided")

        if notification_type == 'new_event':
            profile.notify_on_new_event = target_value
        elif notification_type == 'new_subscription':
            profile.notify_on_new_subscription = target_value
        else:
            raise AttributeError("Invalid 'type' provided")

        profile.save()

        return redirect('profile')


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        if self.object.has_usable_password():
            return PasswordChangeForm
        else:
            # User logged in through a social account
            return SetPasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs

    def form_valid(self, form):
        ret = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return ret
