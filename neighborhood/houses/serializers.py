from rest_framework import serializers

from houses.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'when', 'building', 'location']
