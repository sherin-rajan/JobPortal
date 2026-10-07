from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from jobs.models import Profile


class AdminUserDetailsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.user = User.objects.create_user(
            username="jordan",
            first_name="Jordan",
            last_name="Lee",
            email="jordan@example.com",
            password="test-password",
        )
        self.client.force_login(self.admin)

    def test_user_details_show_account_and_profile_without_edit_controls(self):
        Profile.objects.create(
            user=self.user,
            headline="Software engineer",
            place="Toronto",
            phone="555-0100",
            qualification="BSc",
        )

        response = self.client.get(reverse("user_details", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jordan Lee")
        self.assertContains(response, "jordan@example.com")
        self.assertContains(response, "Software engineer")
        self.assertContains(response, "Toronto")
        self.assertContains(response, "555-0100")
        self.assertContains(response, "BSc")
        self.assertNotContains(response, "Edit Profile")

    def test_user_details_display_missing_profile_fields(self):
        response = self.client.get(reverse("user_details", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not provided")

    def test_user_list_details_button_links_to_user_profile(self):
        response = self.client.get(reverse("view_users"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("user_details", args=[self.user.id])}"',
        )

    def test_user_details_are_limited_to_non_admin_users(self):
        response = self.client.get(reverse("user_details", args=[self.admin.id]))

        self.assertEqual(response.status_code, 404)

    def test_non_admin_cannot_view_user_details(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("user_details", args=[self.user.id]))

        self.assertRedirects(response, reverse("all_jobs"))
