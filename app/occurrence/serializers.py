from rest_framework import serializers

from occurrence.models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = (
            'id',
            'description',
            'author',
            'state',
            'category',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author')


class OccurrenceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = (
            'description',
            'category',
            'author',
            'state',
        )
        read_only_fields = ('author', 'state')


class OccurrenceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = (
            'description',
            'category',
            'author',
            'state',
        )
