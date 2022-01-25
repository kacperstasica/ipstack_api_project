from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Geolocation
from .serializers import GeolocationSerializer


class GeolocationViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = GeolocationSerializer
    queryset = Geolocation.objects.all()
    lookup_field = 'ip_address'
    lookup_value_regex = r'[0-9]+(?:\.[0-9]+){3}|([a-f0-9:]+:+)+[a-f0-9]+'
