from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from management.models import Building, Room, Resident, Event
from .serializers import BuildingSerializer, ResidentListSerializer, RoomSerializer, ResidentSerializer, EventSerializer
from management.permissions import isAdminUser
import logging
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

logger = logging.getLogger(__name__)


def validate_unique_name(model, value):
    if model.objects.filter(name=value).exists():
        raise serializers.ValidationError(f"{model.__name__} with the name '{value}' already exists.")
    return value

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated, isAdminUser]
    throttle_classes = [UserRateThrottle]

    def validate_name(self, value):
        return validate_unique_name(Building, value)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    search_fields = ['name', 'building__name']
    permission_classes = [IsAuthenticated, isAdminUser]

    def validate_name(self, value):
        return validate_unique_name(Room, value)
    
    @method_decorator(cache_page(60 * 60)) # cache for 1 hour
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.select_related('room', 'room__building').all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated, isAdminUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room']

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Resident.DoesNotExist:
            logger.error("Resident not found", exc_info=True)
            raise NotFound("Resident not found.")
        
    def get_resident_list():
        residents = cache.get('resident_list')
        if not residents:
            residents = Resident.object.all()
            cache.set('resident_list', residents, 60 * 60) # cache for 1 hour
        return residents
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResidentListSerializer
        return ResidentSerializer
    
    def get(self, request, resident_id):
        try:
            resident = Resident.objects.get(id=resident_id)
            data = {
                "name": resident.name,
                "decrypted_email": resident.get_decrypted_email(),
                "decrypted_phone": resident.get_decrypted_phone(),
            }
            return Response(data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response({"error": "Resident not found"}, status=status.HTTP_404_NOT_FOUND)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('room', 'room__building').all()
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = [IsAuthenticated, isAdminUser]
    throttle_classes = [UserRateThrottle]

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        room = self.get_object()
        events = Event.objects.filter(room=room)
        if not events.exists():
            return Response({"detail": "No events found for this room."}, status=404)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
