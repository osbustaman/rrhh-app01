from rest_framework import serializers

from applications.company.models import BoxesCompensation, MutualSecurity


class BoxesCompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxesCompensation
        fields = '__all__'

class MutualSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualSecurity
        fields = '__all__'
