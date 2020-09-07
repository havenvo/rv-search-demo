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
    query_service_price = serializers.SerializerMethodField('get_query_service_price')
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_query_service_price(self, obj):
        if self.context:
            service_type = self.context['service_type']
            if service_type is not None:
                return obj.service_rates.filter(service_type__short_code=service_type)[:1].get().price
        return 0

    def get_full_name(self, obj):
        full_name = None
        if obj.first_name or obj.last_name:
            full_name = obj.first_name + " " + obj.last_name
        return full_name

    class Meta:
        model = Profile
        fields = [
            'id',
            'service_rates',
            'first_name',
            'last_name',
            'full_name',
            'title',
            'description',
            'reviews_count',
            'rating_average',
            'avatar',
            'query_service_price'
        ]
        read_only_fields = ['id']
