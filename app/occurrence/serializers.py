from rest_framework import serializers

from occurrence.models import Occurrence, State


class OccurrenceSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Occurrence
        fields = (
            'id',
            'description',
            'author',
            'category',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author')

    def create(self, validated_data):
        occurrence = Occurrence(
            description=validated_data['description'],
            author=validated_data['author'],
            state=State.NOT_VALIDATED,
            category=validated_data['category'],
        )
        occurrence.save()
        return occurrence
