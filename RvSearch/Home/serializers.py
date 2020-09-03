from rest_framework import serializers
from Core.models import Profile, ServiceRate, ServiceType


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'display_name', 'short_code']


class ServiceRateSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer()

    class Meta:
        model = ServiceRate
        fields = ['profile_id', 'service_type_id', 'price', 'currency', 'service_type']


class ProfileSerializer(serializers.ModelSerializer):
    service_rates = ServiceRateSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'service_rates',
            'first_name',
            'last_name',
            'title',
            'description',
            'reviews_count',
            'rating_average',
            'avatar'
        ]
        read_only_fields = ['id']
