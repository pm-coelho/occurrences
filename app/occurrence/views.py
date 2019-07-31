from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from occurrence.models import Occurrence, State

from occurrence.serializers import OccurrenceSerializer, \
                                   OccurrenceCreateSerializer, \
                                   OccurrenceUpdateSerializer


# TODO better handling of PATCH vs PUT

class OccurrenceViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin):

    authentication_classes = (BasicAuthentication,)
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'update': (IsAdminUser,),
        'partial_update': (IsAdminUser,)
    }

    def get_permissions(self):
        """
        Allow for custom permission classes when needed
        """
        try:
            custom_permissions = self.permission_classes_by_action[self.action]
            return [permission() for permission in custom_permissions]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        Return objects for the current authenticated user only except on admins
        """
        queryset = self.queryset

        if (self.action == 'list'):
            author_filter = self.request.query_params.get('author', None)
            if (author_filter):
                queryset = queryset.filter(author=author_filter)

            category_filter = self.request.query_params.get('category', None)
            if (category_filter):
                queryset = queryset.filter(category=category_filter)

        if (self.request.user.is_superuser):
            return queryset
        else:
            return queryset.filter(author=self.request.user)

    def get_serializer_class(self):
        """
        Use different serializers for different endpoints
        """
        if self.action == 'create':
            return OccurrenceCreateSerializer
        elif self.action == 'update':
            return OccurrenceUpdateSerializer
        return OccurrenceSerializer

    def perform_create(self, serializer):
        """
        Auto fill author and state fields on create
        """
        serializer.save(
            author=self.request.user,
            state=State.NOT_VALIDATED.name
        )
