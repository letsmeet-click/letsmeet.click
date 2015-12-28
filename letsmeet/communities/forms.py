from django import forms
from django.template.defaultfilters import slugify

from events.models import Event
from .models import Community


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'begin', 'end', )
        # FIXME find or write a good datetime picker
        # widgets = {
        #     'begin': widgets.AdminDateWidget(),
        #     'end': widgets.AdminDateWidget(),
        # }


class CommunityUpdateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'slug', 'cname', 'twitter', 'github', 'homepage', 'irc_channel', 'irc_network', 'slack', ]

    def clean_slug(self):
        slug = slugify(self.cleaned_data['slug'])
        if Community.objects.exclude(pk=self.instance.pk).filter(slug=slug):
            raise forms.ValidationError("The slug is not unique.")
        return slug
