from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from dynamic_rest.viewsets import DynamicModelViewSet
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter


from base.models import Drone
from base.api.serializers.drones import DroneSerializer


class DroneViewSet(DynamicModelViewSet):
    """
    API endpoint that allows drone to be viewed and edited.
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, ]

    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter,
    ]

    model = Drone
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    def get_queryset(self):
        """
        Filters and sorts models collections.
        """
        queryset = Drone.objects.all()

        return queryset.order_by("serial_number")