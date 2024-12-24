from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation, Ticket
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowListSerializer,
    PlanetariumDomeSerializer,
)

class ModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass123"
        )
        self.show_theme = ShowTheme.objects.create(name="Test Theme")
        self.astronomy_show = AstronomyShow.objects.create(
            title="Test Show",
            description="Test Description"
        )
        self.astronomy_show.show_theme.add(self.show_theme)
        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Test Dome",
            rows=20,
            seats_in_row=30
        )
        self.show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time="2024-03-20 12:00:00"
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            show_session=self.show_session,
            reservation=self.reservation
        )

    def test_show_theme_str(self):
        self.assertEqual(str(self.show_theme), self.show_theme.name)

    def test_astronomy_show_str(self):
        self.assertEqual(str(self.astronomy_show), self.astronomy_show.title)

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass123"
        )
        self.client.force_authenticate(self.user)
        
    def test_show_theme_list(self):
        ShowTheme.objects.create(name="Test Theme")
        response = self.client.get(reverse("planetarium:showtheme-list"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_show_theme(self):
        payload = {"name": "New Theme"}
        response = self.client.post(
            reverse("planetarium:showtheme-list"),
            payload
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exists = ShowTheme.objects.filter(
            name=payload["name"]
        ).exists()
        self.assertTrue(exists)

class SerializerTests(TestCase):
    def test_show_theme_serializer(self):
        show_theme = ShowTheme.objects.create(name="Test Theme")
        serializer = ShowThemeSerializer(show_theme)
        
        self.assertEqual(set(serializer.data.keys()), {"id", "name"})
        self.assertEqual(serializer.data["name"], "Test Theme")

    def test_astronomy_show_list_serializer(self):
        show_theme = ShowTheme.objects.create(name="Test Theme")
        astronomy_show = AstronomyShow.objects.create(
            title="Test Show",
            description="Test Description"
        )
        astronomy_show.show_theme.add(show_theme)
        
        serializer = AstronomyShowListSerializer(astronomy_show)
        self.assertEqual(set(serializer.data.keys()), {"id", "title", "description", "show_theme"})
        self.assertEqual(serializer.data["title"], "Test Show")
        self.assertEqual(serializer.data["show_theme"], ["Test Theme"])
