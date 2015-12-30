from django.contrib.gis import admin
from django import forms
from django.contrib.gis.forms import OpenLayersWidget

from .models import Location


class CDNOpenLayersWidget(OpenLayersWidget):
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js',
            'gis/js/OLMapWidget.js',
        )


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'slug', 'geo_location', 'description', 'notes', 'city', 'country']
        widgets = {
            'geo_location': (CDNOpenLayersWidget),
        }


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    form = LocationAdminForm
    list_display = ['name', 'city', 'country']
