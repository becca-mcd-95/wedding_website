from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Household, Guest
from datetime import date

# Create your tests here.

@override_settings(RSVP_DEADLINE=date(2100, 1, 1))
class NameLookupTests(TestCase):

    def setUp(self):
        invite_type = Household.InviteType.ALL_DAY
        household = Household.objects.create(name="Fake", invite_type=invite_type)
        Guest.objects.create(first_name="Mia", surname="Fake", household=household)
        session = self.client.session
        session["site_unlocked"] = True
        session.save()

    def test_known_name_redirects_to_confirm(self):
        response = self.client.post(
            reverse("search"),
            {"first_name": "Mia", "surname": "Fake"}
        )
        self.assertRedirects(
            response,
            reverse("confirm")
        )

    def test_unknown_name_shows_message(self):
        response = self.client.post(
            reverse("search"),
            {"first_name": "Nobody", "surname": "Here"},
        )
        self.assertContains(response, "couldn't find you")

    @override_settings(RSVP_DEADLINE=date(2000, 1, 1))
    def test_search_after_deadline_shows_closed(self):
        response = self.client.get(reverse("search"))
        self.assertContains(response, "RSVPs have now closed")

@override_settings(RSVP_DEADLINE=date(2100, 1, 1))
class RsvpFlowTest(TestCase):

    def setUp(self):
        household = Household.objects.create(
            name="Fake", invite_type=Household.InviteType.ALL_DAY)
        self.guest = Guest.objects.create(
            first_name="Mia", surname="Fake", household=household)
        session = self.client.session
        session["site_unlocked"] = True
        session.save()

    def search_for_guest(self):
        self.client.post(
            reverse("search"),
            {"first_name": "Mia", "surname": "Fake"},
        )

    def reply_data(self, answer):
        return {
            "guests-TOTAL_FORMS": "1",
            "guests-INITIAL_FORMS": "1",
            "guests-0-id": self.guest.id,
            "guests-0-reply_status": answer,
        }

    def test_reply_without_search_redirects_to_search(self):
        response = self.client.get(
            reverse("reply")
        )
        self.assertRedirects(
            response,
            reverse("search")
        )

    def test_attending_reply_redirects_to_dietary(self):
        self.search_for_guest()
        response = self.client.post(reverse("reply"), self.reply_data("Y"))
        self.assertRedirects(response, reverse("dietary"))

    def test_declined_reply_redirects_to_thanks(self):
        self.search_for_guest()
        response = self.client.post(reverse("reply"), self.reply_data("N"))
        self.assertRedirects(response, reverse("thanks"))

    def dietary_data(self):
        return {
            "guests-TOTAL_FORMS": "1",
            "guests-INITIAL_FORMS": "1",
            "guests-0-id": self.guest.id,
            "guests-0-dietary_notes": "",
        } 

    def test_dietary_redirects_to_accommodation(self):
        self.search_for_guest()
        self.guest.reply_status = "Y"
        self.guest.save()
        response = self.client.post(reverse("dietary"), self.dietary_data())
        self.assertRedirects(response, reverse("accommodation"))

    def accommodation_data(self, needs):
        data = {
            "guests-TOTAL_FORMS": "1",
            "guests-INITIAL_FORMS": "1",
            "guests-0-id": self.guest.id,
        }
        if needs:
            data["guests-0-needs_accommodation"] = "on"
        return data

    def test_needs_accommodation_redirects_to_stay(self):
        self.search_for_guest()
        self.guest.reply_status = "Y"
        self.guest.save()
        response = self.client.post(reverse("accommodation"), self.accommodation_data(True))
        self.assertRedirects(response, reverse("stay"))

    def test_no_accommodation_redirects_to_coach(self):
        self.search_for_guest()
        self.guest.reply_status = "Y"
        self.guest.save()
        response = self.client.post(reverse("accommodation"), self.accommodation_data(False))
        self.assertRedirects(response, reverse("coach"))

    def coach_data(self, choice):
        return {
            "guests-TOTAL_FORMS": "1",
            "guests-INITIAL_FORMS": "1",
            "guests-0-id": self.guest.id,
            "guests-0-coach": choice,
        }

    def test_coach_redirects_to_extras(self):
        self.search_for_guest()
        self.guest.reply_status = "Y"
        self.guest.save()
        response = self.client.post(reverse("coach"), self.coach_data(Guest.Coach.BOTH))
        self.assertRedirects(response, reverse("extras"))

    def test_extras_redirects_to_thanks(self):
            self.search_for_guest()
            self.guest.reply_status = "Y"
            self.guest.save()
            response = self.client.post(reverse("extras"), {"comments": "", "email": ""})
            self.assertRedirects(response, reverse("thanks"))

class SitePasswordTests(TestCase):
    def test_locked_visitor_redirected_to_password(self):
        response = self.client.get(
            reverse("info")
        )
        self.assertRedirects(response, reverse("site_password"))

    @override_settings(SITE_PASSWORD="test-password")
    def test_correct_password_redirects_to_info(self):
        response = self.client.post(
            reverse("site_password"), {"password": "test-password"}
        )
        self.assertRedirects(response, reverse("info"))
