from django import forms

from events.models import Event


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'slug', 'begin', 'end')

    def clean_slug(self):
        if Event.objects.filter(slug=self.cleaned_data['slug'],
                                community=self.instance.community):
            raise forms.ValidationError("The slug is not unique for this community.")
        return self.cleaned_data['slug']
