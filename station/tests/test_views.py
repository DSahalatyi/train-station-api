import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from station.models import CrewMember


class UnauthenticatedStationViewTests(TestCase):
    def test_unauthenticated_stations(self):
        response = self.client.get(reverse("station:station-list"))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_routes(self):
        response = self.client.get(reverse("station:route-list"))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_trains(self):
        response = self.client.get(reverse("station:train-list"))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_crew_member(self):
        response = self.client.get(reverse("station:crewmember-list"))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_trips(self):
        response = self.client.get(reverse("station:trip-list"))
        self.assertEqual(response.status_code, 401)


class AuthenticatedStationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@email.com", password="testpass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_authenticated_stations(self):
        response = self.client.get(reverse("station:station-list"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_routes(self):
        response = self.client.get(reverse("station:route-list"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_trains(self):
        response = self.client.get(reverse("station:train-list"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_crew_member(self):
        response = self.client.get(reverse("station:crewmember-list"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_crew_member_upload_image(self):
        response = self.client.get(
            reverse("station:crewmember-upload-image", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 403)


class AdminStationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@email.com", password="testpass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_admin_crew_member_get_upload_image(self):
        response = self.client.get(
            reverse("station:crewmember-upload-image", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 405)

    def test_admin_crew_member_post_upload_image(self):
        crew = CrewMember.objects.create(first_name="Test", last_name="Testing")

        url = reverse("station:crewmember-upload-image", kwargs={"pk": crew.pk})

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            response = self.client.post(url, {"image": ntf}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        crew.refresh_from_db()
        self.assertTrue(crew.image)
        self.assertRegex(str(crew.image), r"upload/crew/test-testing-[a-f0-9\-]+\.jpg")
