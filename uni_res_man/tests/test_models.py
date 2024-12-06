import pytest
from django.contrib.auth.models import User
from management.models import Building, Room, Resident


@pytest.mark.django_db
def test_building_creation():
    building = Building.objects.create(name="Building 1", address="123 Main St")
    assert building.name == "Building 1"
    assert building.address == "123 Main St"
    assert Building.objects.count() == 1


@pytest.mark.django_db
def test_room_creation():
    building = Building.objects.create(name="Building 1", address="123 Main St")
    room = Room.objects.create(name="Room 1", building=building, capacity=4)
    assert room.name == "Room 1"
    assert room.building == building
    assert room.capacity == 4
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_resident_creation():
    building = Building.objects.create(name="Building 1", address="123 Main St")
    room = Room.objects.create(name="Room 1", building=building, capacity=4)
    resident = Resident.objects.create(
        name="John Doe", room=room, phone="123-456-7890", email="WqO4h@example.com"
    )
    assert resident.name == "John Doe"
    assert resident.room == room
    assert resident.email != ""
    assert resident.phone != ""
    assert Resident.objects.count() == 1