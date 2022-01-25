from rest_framework import serializers

from .models import Geolocation, Language
from .services.geo_locator import GeoLocator


class GeolocationSerializer(serializers.ModelSerializer):
    languages = serializers.StringRelatedField(read_only=True, many=True)
    ip_address = serializers.IPAddressField(max_length=45)

    class Meta:
        model = Geolocation
        fields = [
            'ip_address', 'continent_name', 'country_name',
            'region_name', 'city', 'zip', 'latitude',
            'longitude', 'languages',
        ]
        read_only_fields = (
            'continent_name', 'country_name', 'region_name',
            'city', 'zip', 'latitude', 'longitude',
        )

    def create(self, validated_data):
        ip_address = validated_data['ip_address']

        geo_locator = GeoLocator(ip_address=ip_address)
        location, geolocation = geo_locator.data.pop('location'), geo_locator.data

        languages_to_be_created = location.get('languages')
        languages = []
        for language in languages_to_be_created:
            clean_language = self.get_clean_dict(language)
            obj, c = Language.objects.get_or_create(**clean_language)
            languages.append(obj)

        clean_geolocation = self.get_clean_dict(geolocation)
        instance = Geolocation.objects.create(
            ip_address=ip_address,
            **clean_geolocation
        )

        if languages:
            instance.languages.add(*languages)
        return instance

    @staticmethod
    def validate_ip_address(ip_address):
        if Geolocation.objects.filter(ip_address__exact=ip_address).exists():
            raise serializers.ValidationError(
                'We already have such geolocation in our database.'
            )
        return ip_address

    @staticmethod
    def get_clean_dict(dictionary):
        return {key: value for key, value in dictionary.items() if value}
