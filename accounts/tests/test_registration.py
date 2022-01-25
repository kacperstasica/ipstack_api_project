from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {
            "email": "ipstack-test@project.com",
            "password": "Tymczasowe!@",
            "confirm_password": "Tymczasowe!@"
        }

    def test_register_superuser(self):
        response = self.client.post(
            path=reverse('register'),
            data=self.user_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('rest_framework_simplejwt.serializers.TokenObtainPairSerializer.get_token')
    @patch('rest_framework_simplejwt.serializers.TokenObtainPairSerializer.validate')
    def test_obtain_token(self, mock_token, mock_validation):
        mock_token.return_value = {'access': 'asdf1234', 'refresh': 'asdf4321'}
        mock_validation.return_value = {'access': 'asdf1234', 'refresh': 'asdf4321'}

        response = self.client.post(
            path=reverse('token_obtain_pair'),
            data={
                'email': self.user_data['email'],
                'password': self.user_data['password']
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('access'), 'asdf1234')
        self.assertEqual(response.json().get('refresh'), 'asdf4321')

    def test_register_superuser_no_password(self):

        response = self.client.post(
            path=reverse('register'),
            data={'email': self.user_data['email'], 'password': ''},
            format='json',
        )

        self.assertIn(
            'This field may not be blank.',
            response.json().get('password')
        )

    def test_register_superuser_password_too_short(self):
        self.user_data['password'] = 'a1b2c3d'
        self.user_data['confirm_password'] = 'a1b2c3d'

        response = self.client.post(
            path=reverse('register'),
            data=self.user_data,
            format='json',
        )

        self.assertIn(
            'This password is too short. It must contain at least 8 characters.',
            response.json().get('password')
        )

    def test_register_superuser_password_too_common(self):
        response = self.client.post(
            path=reverse('register'),
            data={
                'email': self.user_data['email'],
                'password': '123456789',
                'confirm_password': '123456789'
            },
            format='json',
        )

        self.assertIn(
            'This password is too common.',
            response.json().get('password')
        )

    def test_confirm_password_not_matching_raises_validation_error(self):
        response = self.client.post(
            path=reverse('register'),
            data={
                'email': self.user_data['email'],
                'password': self.user_data['password'],
                'confirm_password': 'asdf1234'
            },
            format='json',
        )

        self.assertIn(
            'Passwords must match.',
            response.json().get('password')
        )
