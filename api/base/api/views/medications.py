from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from dynamic_rest.viewsets import DynamicModelViewSet
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter


from base.models import Medication
from base.api.serializers.medications import MedicationSerializer


class MedicationViewSet(DynamicModelViewSet):
    """
    API endpoint that allows medications to be viewed and edited.
    """

    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, ]

    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter,
    ]

    model = Medication
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def get_queryset(self):
        """
        Filters and sorts medications.
        """
        queryset = Medication.objects.all()

        return queryset.order_by("name")