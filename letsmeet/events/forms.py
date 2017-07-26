from django import forms
from django.template.defaultfilters import slugify
from django.conf import settings

from events.models import Event, EventComment
from locations.models import Location


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'begin', 'end', 'max_attendees']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(settings, 'SHACKSPACE'):
            self.fields['location'] = forms.ModelChoiceField(queryset=Location.objects.all(),
                                                             empty_label=None, widget=forms.RadioSelect, required=True)
        # FIXME find or write a good datetime picker
        # widgets = {
        #     'begin': widgets.AdminDateWidget(),
        #     'end': widgets.AdminDateWidget(),
        # }


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'slug', 'description', 'begin', 'end', 'twitter_hashtag', 'max_attendees')

    def clean_slug(self):
        slug = slugify(self.cleaned_data['slug'])
        if Event.objects.exclude(pk=self.instance.pk)\
                        .filter(slug=slug, community=self.instance.community):
            raise forms.ValidationError('The slug ("{}") is not unique for this community.'.format(slug))
        return slug

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('end', 0) < cleaned_data.get('begin', 1):
            self.add_error('end', forms.ValidationError('End cannot be before begin'))

        return cleaned_data


class EventCommentCreateForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ('text', )
