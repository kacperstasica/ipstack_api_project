from django.contrib import admin

from geolocations.models import Geolocation


@admin.register(Geolocation)
class GeolocationAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address', 'country_name', 'city'
    )
    readonly_fields = (
        'ip_address', 'continent_name', 'country_name',
        'region_name', 'city', 'zip', 'latitude', 'longitude',
        'languages'
    )

    fieldsets = (
        ('Geolokalizacja - dane', {
            'fields': (
                'ip_address', 'continent_name', 'country_name',
                'region_name', 'city', 'zip',
                ('latitude', 'longitude')
            ),
        }),
        ('Języki', {
            'fields': ('languages',),
        }),
    )
