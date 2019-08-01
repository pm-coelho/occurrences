from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField

from occurrence.models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Occurrence
        fields = (
            'id',
            'description',
            'author',
            'state',
            'category',
            'location',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author')


class OccurrenceCreateSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Occurrence
        fields = (
            'description',
            'category',
            'author',
            'state',
            'location',
        )
        read_only_fields = ('author', 'state')


class OccurrenceUpdateSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Occurrence
        fields = (
            'description',
            'category',
            'author',
            'state',
            'location',
        )
