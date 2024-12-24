from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from django.utils.decorators import method_decorator

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    TicketSerializer,
    AstronomyShowRetrieveSerializer,
    AstronomyShowListSerializer,
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer,
    TicketListSerializer,
    TickerRetrieveSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("show_theme")

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer
        return AstronomyShowSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.prefetch_related("astronomy_show", "planetarium_dome")
        if self.action == "retrieve":
            return queryset.prefetch_related(
                "astronomy_show__show_theme", "planetarium_dome"
            )

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer
        return ShowSessionSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email"]

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        if self.action == "list":
            return queryset.prefetch_related("user")
        return queryset

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["row", "seat", "reservation__user__email", "show_session__astronomy_show__title"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related(
                "show_session__astronomy_show",
                "reservation__user",
            )

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TickerRetrieveSerializer
        return TicketSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="ticket_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
