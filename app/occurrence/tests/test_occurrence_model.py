from django.test import TestCase
from django.contrib.auth import get_user_model

from occurrence.models import Occurrence


def sample_user(username='test_user', password='testpass'):
    """Create sample test user"""
    return get_user_model().objects.create_user(username, password)


class OccurrenceModelTests(TestCase):
    def test_occurrence_str(self):
        """Test the occurrence string representation"""
        occurrence = Occurrence.objects.create(
            author=sample_user(),
            description='this is a test'
        )

        self.assertEqual(str(occurrence), occurrence.description)
