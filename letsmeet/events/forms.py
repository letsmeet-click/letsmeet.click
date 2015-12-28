from django import forms
from django.template.defaultfilters import slugify

from events.models import Event


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'slug', 'begin', 'end')

    def clean_slug(self):
        slug = slugify(self.cleaned_data['slug'])
        if Event.objects.exclude(pk=self.instance.pk)\
                        .filter(slug=slug, community=self.instance.community):
            raise forms.ValidationError('The slug ("{}") is not unique for this community.'.format(slug))
        return slug
