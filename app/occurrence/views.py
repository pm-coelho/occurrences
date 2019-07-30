from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from occurrence.models import Occurrence, State

from occurrence import serializers


class OccurrenceViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Occurrence.objects.all()
    serializer_class = serializers.OccurrenceSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        if (self.request.user.is_superuser):
            return self.queryset
        else:
            return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, state=State.NOT_VALIDATED)
