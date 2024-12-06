import pytest
from rest_framework.exceptions import ValidationError
from core.serializers import RoomSerializer
from management.models import Building, Room


@pytest.mark.django_db
def test_room_serializer():
    building = Building.objects.create(name="Building 1", address="123 Main St")
    data = {
        "name": "Room 1",
        "building": building.id,
        "capacity": 4,
    }
    serializer = RoomSerializer(data=data)
    assert serializer.is_valid()
    room = serializer.save()
    assert room.name == "Room 1"
    assert room.building == building
    assert room.capacity == 4
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_invalid_capacity_serializer():
    building = Building.objects.create(name="Building 1", address="123 Main St")
    data = {
        "name": "Room 1",
        "building": building.id,
        "capacity": 5,
    }
    serializer = RoomSerializer(data=data)
    assert not serializer.is_valid()
    assert 'capacity' in serializer.errors
