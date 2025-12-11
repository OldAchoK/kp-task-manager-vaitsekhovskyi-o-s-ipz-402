from django.test import SimpleTestCase, Client as TestClient, modify_settings, override_settings
from django.urls import reverse
from unittest.mock import patch, MagicMock
import psycopg
from core.models import Client as ClientModel

@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.file')
@modify_settings(MIDDLEWARE={'remove': 'core.middleware.RoleSwitchMiddleware'})
class CustomLoginNoDBTest(SimpleTestCase):
    
    def setUp(self):
        self.client = TestClient()
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

        self.fake_user = MagicMock()
        self.fake_user.clientid = 123
        self.fake_user.role = 'manager'
        self.fake_user.email = 'test@example.com'

    @patch('core.models.Client.objects.get')
    @patch('psycopg.connect') 
    def test_login_success(self, mock_connect, mock_get_user):
        """Тест успішного входу"""
        mock_get_user.return_value = self.fake_user
        mock_connect.return_value.__enter__.return_value = MagicMock()

        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'any_password'
        })

        self.assertRedirects(response, self.dashboard_url, fetch_redirect_response=False)
        self.assertEqual(self.client.session['user_id'], 123)

    @patch('core.models.Client.objects.get')
    @patch('psycopg.connect')
    def test_login_wrong_password(self, mock_connect, mock_get_user):
        """Тест неправильного пароля"""
        mock_get_user.return_value = self.fake_user
        mock_connect.side_effect = psycopg.OperationalError("Wrong password")

        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrong'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Incorrect password')

    @patch('core.models.Client.objects.get')
    def test_user_not_found(self, mock_get_user):
        """Тест неіснуючого користувача"""
        mock_get_user.side_effect = ClientModel.DoesNotExist

        response = self.client.post(self.login_url, {
            'email': 'unknown@example.com',
            'password': 'any'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'User not found')