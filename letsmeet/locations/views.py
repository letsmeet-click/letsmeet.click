from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from opencage.geocoder import OpenCageGeocode
from django.conf import settings


class SearchForm(forms.Form):
    search = forms.CharField(max_length=1000)


class LocationSearchView(FormView):
    template_name = 'locations/locations_create.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = self.get_form(self.form_class)
        if form.is_valid():
            geocoder = OpenCageGeocode(settings.OPEN_CAGE_GEOCODER)
            search = form.cleaned_data['search']
            result = geocoder.geocode(search)
            context['result'] = result
        return render(self.request, self.template_name, context)
