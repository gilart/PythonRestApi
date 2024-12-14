from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from time import sleep

class AuthTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        cls.client = APIClient()

    def test_token_obtain_and_user_info(self):
        # Get token
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

        access_token = data['access']
        refresh_token = data['refresh']

        # Sprawdzenie dostępu do /api/user/ z access tokenem
        response = self.client.get('/api/user/', HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())

        # Czekamy ponad 1 minutę, aby token wygasł (lub zmień czas na krótszy w testach)
        sleep(61)
        # Teraz token powinien być nieważny
        response = self.client.get('/api/user/', HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, 401)

        # Odświeżamy access token za pomocą refresh
        response = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, 200)
        new_access_token = response.json()['access']
        refresh_token = response.json()['refresh']

        # Sprawdź dostęp z nowym access tokenem
        response = self.client.get('/api/user/', HTTP_AUTHORIZATION=f'Bearer {new_access_token}', format='json')
        self.assertEqual(response.status_code, 200)

        # Wylogowanie (unieważnienie refresh tokenu)
        response = self.client.post('/api/logout/', {'refresh': refresh_token}, HTTP_AUTHORIZATION=f'Bearer {new_access_token}', format='json')
        print(refresh_token)
        self.assertEqual(response.status_code, 200)

        # Ponowna próba odświeżenia tokenu powinna się nie udać
        response = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')
        self.assertNotEqual(response.status_code, 200)
