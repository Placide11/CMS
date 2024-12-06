from rest_framework import serializers
from management.models import Building, Room, Resident, Event

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'address']

    def validate_name(self, value):
        if Building.objects.filter(name=value).exists():
            raise serializers.ValidationError("Building with this name already exists.")
        return value

    def validate_address(self, value):
        if Building.objects.filter(address=value).exists():
            raise serializers.ValidationError("Building with this address already exists.")
        return value


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'building', 'capacity']

    def validate_name(self, value):
        if Room.objects.filter(name=value).exists():
            raise serializers.ValidationError("Room with this name already exists.")
        return value

    def validate_building(self, value):
        if not Building.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Building does not exist.")
        return value

    def validate_capacity(self, value):
        if value > 4:
            raise serializers.ValidationError("Capacity must be less than or equal to 4.")
        return value


class ResidentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['name']

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['name', 'decrypted_email', 'decrypted_phone']

    def get_decrypted_email(self, obj):
        return obj.get_decrypted_email()

    def get_decrypted_phone(self, obj):
        return obj.get_decrypted_phone()

    def validate_name(self, value):
        if not Resident.objects.filter(name=value).exists():
            raise serializers.ValidationError("Resident with this name does not exist.")
        return value

    def validate_decrypted_email(self, value):
        if not Resident.objects.filter(decrypted_email=value).exists():
            raise serializers.ValidationError("Resident with this email does not exist.")
        return value

    def validate_decrypted_phone(self, value):
        if not Resident.objects.filter(decrypted_phone=value).exists():
            raise serializers.ValidationError("Resident with this phone does not exist.")
        return value


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_time', 'end_time', 'room']

    def validate_room(self, value):
        if not Room.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Room does not exist.")
        return value

        
