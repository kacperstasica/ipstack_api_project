from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory
from geolocations.models import Geolocation, Language
from geolocations.tests.factories import GeolocationFactory


class GeolocationTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.ip_address_v4 = "127.0.0.1"
        cls.ip_address_v6 = "2a03:2880:f12f:83:face:b00c:0:25da"
        cls.ga = 'ga'
        cls.irish = "Irish"
        cls.gaelige = 'Gaeilge'
        cls.en = 'en'
        cls.english = 'English'

    def setUp(self):
        self.client.force_authenticate(user=self.user)
        self.data = {
            "location": {
                "languages": [
                    {
                        "code": self.ga,
                        "name": self.irish,
                        "native": self.gaelige
                    },
                    {
                        "code": self.en,
                        "name": self.english,
                        "native": self.english
                    }
                ]
            },
            "longitude": -6.243333339691162,
            "latitude": 53.35388946533203,
            "zip": None,
            "city": "Dublin",
            "region_name": "Leinster",
            "country_name": "Ireland",
            "continent_name": "Europe",
        }

    @patch('geolocations.services.geo_locator.GeoLocator.get_ip_stack_response')
    def test_add_geolocation_with_ipv4_address(self, mock_response):
        mock_response.return_value = self.data

        self.assertFalse(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        response = self.client.post(
            path=reverse('geolocation-list'),
            data={
                'ip_address': self.ip_address_v4,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        geolocation = Geolocation.objects.get(ip_address=self.ip_address_v4)
        geolocation.refresh_from_db()

        self.assertQuerysetEqual(
            list(geolocation.languages.all()),
            Language.objects.filter(related_geolocations=geolocation)
        )

    @patch('geolocations.services.geo_locator.GeoLocator.get_ip_stack_response')
    def test_add_geolocation_with_ipv6_address(self, mock_response):
        mock_response.return_value = self.data
        self.assertFalse(
            Geolocation.objects.filter(ip_address=self.ip_address_v6).exists()
        )
        response = self.client.post(
            path=reverse('geolocation-list'),
            data={'ip_address': self.ip_address_v6},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Geolocation.objects.filter(ip_address=self.ip_address_v6).exists()
        )

    def test_cannot_add_geolocation_with_invalid_ip_address(self):
        response = self.client.post(
            path=reverse('geolocation-list'),
            data={'ip_address': '1.2.3.4.5.6.7.8.9'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'Enter a valid IPv4 or IPv6 address.',
            response.json().get('ip_address')
        )

    def test_add_geolocation_that_is_already_in_db_raises_validation_error(self):
        GeolocationFactory(ip_address=self.ip_address_v4)
        self.assertTrue(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        response = self.client.post(
            reverse('geolocation-list'),
            data={'ip_address': self.ip_address_v4},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            'We already have such geolocation in our database.',
            response.json().get('ip_address')
        )

    def test_delete_geolocation(self):
        GeolocationFactory(ip_address=self.ip_address_v4)
        self.assertTrue(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        response = self.client.delete(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

    def test_delete_geolocation_that_is_not_in_the_db(self):
        GeolocationFactory(ip_address=self.ip_address_v4)
        self.assertTrue(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        self.client.delete(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        self.assertFalse(
            Geolocation.objects.filter(ip_address=self.ip_address_v4).exists()
        )

        response = self.client.delete(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_get_geolocation(self):
        GeolocationFactory(ip_address=self.ip_address_v4)

        response = self.client.get(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_non_existing_geolocation(self):
        GeolocationFactory(ip_address=self.ip_address_v4)
        self.client.delete(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        response = self.client.get(
            reverse('geolocation-detail', kwargs={
                'ip_address': self.ip_address_v4
            }), format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
