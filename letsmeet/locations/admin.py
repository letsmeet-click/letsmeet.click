from django.contrib.gis import admin

from .models import Location


class CDNOSMGeoAdmin(admin.OSMGeoAdmin):
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'


@admin.register(Location)
class LocationAdmin(CDNOSMGeoAdmin):
    list_display = ['name', 'city', 'country']
