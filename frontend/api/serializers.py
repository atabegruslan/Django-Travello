from rest_framework import serializers
from frontend.models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'img', 'desc', 'price', 'offer']