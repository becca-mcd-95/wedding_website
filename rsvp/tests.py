from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class NameLookupTests(TestCase):

    def test_unknown_name_shows_message(self):
        response = self.client.post(
            reverse("index"),
            {"first_name": "Nobody", "surname": "Here"},
        )
        self.assertContains(response, "couldn't find you")