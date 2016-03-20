from django import forms
from django.template.defaultfilters import slugify

from .models import Community


class CommunityUpdateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            'name', 'slug', 'description', 'cname', 'twitter', 'github', 'homepage', 'irc_channel', 'irc_network',
            'slack', ]

    def clean_slug(self):
        slug = slugify(self.cleaned_data['slug'])
        if Community.objects.exclude(pk=self.instance.pk).filter(slug=slug):
            raise forms.ValidationError("The slug is not unique.")
        return slug
