import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from management.models import Building, Room, Resident
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_login_view():
    client = APIClient()
    resident = Resident.objects.create_user(name="test", email="test@example.com", password="password")
    data = {"email": resident.email, "password": "password"}

    response = client.post(reverse("login"), data)

# @pytest.mark.django_db
# def test_get_room_list():
#     client = APIClient()
#     building = Building.objects.create(name="Building 1", address="123 Main St")
#     Room.objects.create(name="Room 1", building=building, capacity=4)
    
#     response = client.get(reverse("room_list"))
#     assert response.status_code == 200
#     assert len(response.data) == 1
#     assert response.data[0]["name"] == "Room 1"
