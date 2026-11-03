from django.test import TestCase
from django.urls import reverse
from .models import Household, Guest

# Create your tests here.

class NameLookupTests(TestCase):

    def setUp(self):
        invite_type = Household.InviteType.ALL_DAY
        household = Household.objects.create(name="Fake", invite_type=invite_type)
        Guest.objects.create(first_name="Mia", surname="Fake", household=household)

    def test_known_name_redirects_to_confirm(self):
        response = self.client.post(
            reverse("index"),
            {"first_name": "Mia", "surname": "Fake"}
        )
        self.assertRedirects(
            response,
            reverse("confirm")
        )

    def test_unknown_name_shows_message(self):
        response = self.client.post(
            reverse("index"),
            {"first_name": "Nobody", "surname": "Here"},
        )
        self.assertContains(response, "couldn't find you")

class ReplyPageTest(TestCase):

    def setUp(self):
        household = Household.objects.create(
            name="Fake", invite_type=Household.InviteType.ALL_DAY)
        self.guest = Guest.objects.create(
            first_name="Mia", surname="Fake", household=household)

    def search_for_guest(self):
        self.client.post(
            reverse("index"),
            {"first_name": "Mia", "surname": "Fake"},
        )

    def reply_data(self, answer):
        return {
            "guests-TOTAL_FORMS": "1",
            "guests-INITIAL_FORMS": "1",
            "guests-0-id": self.guest.id,
            "guests-0-reply_status": answer,
        }

    def test_reply_without_search_redirects_to_index(self):
        response = self.client.get(
            reverse("reply")
        )
        self.assertRedirects(
            response,
            reverse("index")
        )

    def test_attending_reply_redirects_to_dietary(self):
        self.search_for_guest()
        response = self.client.post(reverse("reply"), self.reply_data("Y"))
        self.assertRedirects(response, reverse("dietary"))

    def test_declined_reply_redirects_to_thanks(self):
        self.search_for_guest()
        response = self.client.post(reverse("reply"), self.reply_data("N"))
        self.assertRedirects(response, reverse("thanks")) 