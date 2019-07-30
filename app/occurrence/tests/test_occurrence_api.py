from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from occurrence.models import Occurrence


OCCURRENCES_URL = reverse('occurrence:occurrence-list')


class PublicOccurrenceApiTests(TestCase):
    """Test public endpoint on occurrence API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_on_get_list(self):
        """Test only admins can get the list of occurrences"""
        res = self.client.get(OCCURRENCES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOccurrenceApiTests(TestCase):
    """Test private endpoints on occurrence API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test_user',
            '12345678'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_occurrences_limited_to_user_self(self):
        """Test that when not admin the user can only see himself"""
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )

        Occurrence.objects.create(author=self.user, description='test_1')
        Occurrence.objects.create(author=user2, description='test_2')

        res = self.client.get(OCCURRENCES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['description'], 'test_1')

    def test_create_occurrence_successfull(self):
        """Test user can create occurrences"""
        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        self.client.post(OCCURRENCES_URL, payload)

        exists = Occurrence.objects.filter(
            author=self.user,
            description=payload['description']
        ).exists()

        self.assertTrue(exists)

    def test_create_occurrence_does_not_allow_state(self):
        pass

    def test_create_occurrence_only_allow_valid_categories(self):
        pass


class AdminOccurrenceAPITests(TestCase):
    """Test admin endpoints on occurrence API"""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='test_admin',
            email='test@admin.com',
            password='12345678',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_admin_can_see_all_occurrence(self):
        """Test only admins can get the list of occurrences"""
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )

        Occurrence.objects.create(author=self.user, description='test_1')
        Occurrence.objects.create(author=user2, description='test_2')

        res = self.client.get(OCCURRENCES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
