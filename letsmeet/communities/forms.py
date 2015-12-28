from django import forms

from events.models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'begin', 'end', )
        # FIXME find or write a good datetime picker
        # widgets = {
        #     'begin': widgets.AdminDateWidget(),
        #     'end': widgets.AdminDateWidget(),
        # }
