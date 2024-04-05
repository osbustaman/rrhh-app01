from rest_framework import serializers

from applications.company.models import BoxesCompensation


class BoxesCompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxesCompensation
        fields = '__all__'
