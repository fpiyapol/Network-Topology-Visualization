from rest_framework import serializers
from .models import Device, Link, Management, Interface

class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = ('port', 'ip_addr', 'n_hostname', 'n_interface')

class DeviceSerializer(serializers.Serializer):
    hostname = serializers.CharField(max_length=255)
    device_type = serializers.CharField(max_length=1)
    # interfaces = serializers.StringRelatedField(many=True)
    interfaces = InterfaceSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Device.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.ip_addr = validated_data.get('ip_addr', instance.ip_addr)

        instance.save()
        return instance

class LinkSerializer(serializers.Serializer):
    coord1 = serializers.CharField(max_length=255)
    coord2 = serializers.CharField(max_length=255)
    interface1 = serializers.CharField(max_length=255)
    interface2 = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Link.objects.create(**validated_data)

class ManagementSerializer(serializers.Serializer):
    ip_addr = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    en_pass = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Management.objects.create(**validated_data)

