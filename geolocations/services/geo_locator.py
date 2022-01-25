import requests
from rest_framework import status

from config.settings import IP_STACK_ACCESS_KEY
from geolocations.exceptions import IPStackConnectionError


class GeoLocator:
    """
    This service uses STACK IP API endpoint to
    gather data on the basis of ipv4 or ipv6 address.
    """
    IP_STACK_BASE_URL = \
        'http://api.ipstack.com/{}?access_key={}&output=json' \
        '&fields=continent_name,country_name,region_name,' \
        'city,zip,latitude,longitude,location.languages'

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.data = self.get_ip_stack_response()

    def get_ip_stack_response(self):
        response = requests.get(
            url=self.IP_STACK_BASE_URL.format(self.ip_address, IP_STACK_ACCESS_KEY)
        )

        if response.status_code != status.HTTP_200_OK:
            raise IPStackConnectionError()
        return response.json()
