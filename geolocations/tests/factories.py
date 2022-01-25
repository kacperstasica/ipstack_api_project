import factory

from geolocations.models import Geolocation, Language


class GeolocationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Geolocation


class LanguageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Language
