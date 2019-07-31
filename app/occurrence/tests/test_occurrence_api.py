from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from occurrence.models import Occurrence


OCCURRENCES_URL = reverse('occurrence:occurrence-list')


# TODO: allow populate of authors
class PublicOccurrenceApiTests(TestCase):
    """Test public endpoint on occurrence API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_on_get_list(self):
        """Test only admins can get the list of occurrences"""
        res = self.client.get(OCCURRENCES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_create_occurrences(self):
        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        res = self.client.post(OCCURRENCES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_patch_occurrence(self):
        user = get_user_model().objects.create_user(
            'test_user',
            '12345678'
        )
        occurrence = Occurrence.objects.create(
            author=user,
            description='test_1',
        )

        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        res = self.client.patch(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_update_occurrences(self):
        user = get_user_model().objects.create_user(
            'test_user',
            '12345678'
        )
        occurrence = Occurrence.objects.create(
            author=user,
            description='test_1',
        )

        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        res = self.client.put(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOccurrenceApiTests(TestCase):
    """Test normal user endpoints on occurrence API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test_user',
            '12345678'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # GET list endpoint tests
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


    def test_user_cannot_use_qs_to_get_other_user_occurrences(self):
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )
        Occurrence.objects.create(author=self.user, category='CONSTRUCTION')
        Occurrence.objects.create(author=user2, description='ROAD_CONDITION')

        res = self.client.get(OCCURRENCES_URL, {'author': user2.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    # POST endpoint tests
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

    def test_create_occurrence_ignores_state(self):
        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
            'state': 'VALID'
        }

        self.client.post(OCCURRENCES_URL, payload)

        exists = Occurrence.objects.filter(
            author=self.user,
            description=payload['description']
        ).exists()

        self.assertTrue(exists)

    def test_create_occurrence_only_allow_valid_categories(self):
        """Test user can create occurrences"""
        payload = {
            'description': 'test_1',
            'category': 'NON_EXISTING',
        }

        res = self.client.post(OCCURRENCES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # PATCH endpoint tests
    def test_user_cannot_patch_occurrence(self):
        occurrence = Occurrence.objects.create(
            author=self.user,
            description='test_1',
        )

        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        res = self.client.patch(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # PUT endpoint tests
    def test_user_cannot_update_occurrence(self):
        """Test user can create occurrences"""
        occurrence = Occurrence.objects.create(
            author=self.user,
            description='test_1',
        )

        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
        }

        res = self.client.put(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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

    # GET list endpoint tests
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

    def test_can_filter_by_author(self):
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )
        Occurrence.objects.create(author=self.user, description='test_1')
        Occurrence.objects.create(author=user2, description='test_2')

        res = self.client.get(OCCURRENCES_URL, {'author': user2.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['author'], user2.id)

    def test_can_filter_by_category(self):
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )
        Occurrence.objects.create(author=self.user, category='CONSTRUCTION')
        Occurrence.objects.create(author=user2, description='ROAD_CONDITION')

        res = self.client.get(OCCURRENCES_URL, {'category': 'CONSTRUCTION'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['category'], 'CONSTRUCTION')

    # POST endpoint tests
    def test_admin_can_create_occurrences(self):
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

    # PATCH endpoint tests
    def test_admin_can_patch_state(self):
        occurrence = Occurrence.objects.create(
            author=self.user,
            description='test_1',
            state='NOT_VALIDATED'
        )

        payload = {'state': 'VALIDATED'}

        res = self.client.patch(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['state'], payload['state'])

    def test_only_valid_states_are_allowed(self):
        occurrence = Occurrence.objects.create(
            author=self.user,
            description='test_1',
            state='NOT_VALIDATED'
        )

        payload = {'state': 'INVALID_STATE'}

        res = self.client.patch(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # PUT endpoint tests
    def test_admin_can_update_occurrences(self):
        """Test user can create occurrences"""
        user2 = get_user_model().objects.create_user(
            'other',
            '12345678'
        )
        occurrence = Occurrence.objects.create(
            author=self.user,
            description='test_1',
        )

        payload = {
            'description': 'test_1',
            'category': 'CONSTRUCTION',
            'state': 'RESOLVED',
            'author': user2.id,
        }

        res = self.client.put(
            '{}{}/'.format(OCCURRENCES_URL, occurrence.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
