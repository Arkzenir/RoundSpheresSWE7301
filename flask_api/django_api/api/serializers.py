from rest_framework import serializers
from .models import SciRecord

class SciRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SciRecord
        fields = '__all__'  # Serialise whole record
        extra_kwargs = {
            'id': {'required': False}
        }