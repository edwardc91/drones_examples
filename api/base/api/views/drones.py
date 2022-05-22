from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from dynamic_rest.viewsets import DynamicModelViewSet
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter

from django.db.models import Q
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from base.models import Drone, Flight, Load, Medication
from base.api.serializers.drones import DroneSerializer, DroneBatterySerializer, DroneLoadSerializer, DroneAddLoadSerializer, DroneCurrentLoadSerializer
from base.api.serializers.errors import ErrorSerializer


class DroneViewSet(DynamicModelViewSet):
    """
    API endpoint that allows drone to be viewed and edited.
    """

    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, ]

    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter,
    ]

    model = Drone
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    def get_queryset(self):
        """
        Filters and sorts drones.
        """
        queryset = Drone.objects.all()

        return queryset.order_by("serial_number")


    @extend_schema(methods=['get'], responses={200: DroneBatterySerializer()},
                   description="API endpoint allowing to retrieve the battery for a drone.")
    @action(detail=True, methods=['get'])
    def battery(self, request, pk=None):
        drone = self.get_object()
        return Response(DroneBatterySerializer(embed=True, many=True).to_representation(drone))


    @extend_schema(methods=['get'], responses={200: DroneCurrentLoadSerializer()},
                   description="API endpoint allowing to retrieve the current load weight for a drone.")
    @action(detail=True, methods=['get'])
    def current_load_weight(self, request, pk=None):
        drone = self.get_object()
        return Response(DroneCurrentLoadSerializer({"current_load": drone.get_load_weight()}).data, status=200)


    @extend_schema(methods=['get'], responses={200: DroneLoadSerializer()},
                   description="API endpoint allowing to retrieve the load for a drone.")
    @action(detail=True, methods=['get'])
    def load(self, request, pk=None):
        drone = self.get_object()
        flights = drone.flights_rel.filter(was_delivered=False)
        loads = {}
        if flights.exists():
            loads = flights[0].loads_rel
        return Response(DroneLoadSerializer(embed=True, many=True).to_representation(loads))

    
    @extend_schema(
        methods=['patch'], 
        responses={
            200: DroneLoadSerializer(),
            422: ErrorSerializer()
        },
        request=DroneAddLoadSerializer(many=False),
        description="API endpoint allowing to add load to a drone.")
    @action(detail=True, methods=['patch'])
    @transaction.atomic
    def load_addition(self, request, pk=None):
        """
        Adds load to a drone.
        # This endpoint allows add new load to a drone available
        * If the drone is on IDLE state a new Flight is created with the load in the payload
        * If the drone is on LOADING state and do not exists a load for the medication in the payload a new load is created, if exists the load quanity is updated with the current quanty plus the quantity on the payload
        """

        drone = self.get_object()

        serializer = DroneAddLoadSerializer(data=request.data, many=False)

        if serializer.is_valid():
            medication=None
            load_data = serializer.data
            try:
                medication=Medication.objects.get(pk=load_data['medication'])
            except Medication.DoesNotExist:
                return Response({'details': _('Medication does not exists on database')}, status=400)

            if drone.state == 'IDLE' and drone.battery_capacity >= 25:
                drone.state='LOADING'
                flight = Flight.objects.create(
                    drone_rel=drone,
                )

                if drone.weight_limit >= load_data['quantity'] * medication.weight:
 
                    Load.objects.create(
                        flight_rel=flight,
                        quantity=load_data['quantity'],
                        medication_rel=medication
                    )
                else:
                    return Response({'details': _('The load is higher that the current weight capacity of the drone')}, status=400)
                drone.save()
            elif drone.state == 'LOADING':
                if drone.get_load_weight() + load_data['quantity'] * medication.weight <= drone.weight_limit:
                    flight = Flight.objects.filter(drone_rel__id=drone.id, was_delivered=False)
                    old_load = flight[0].loads_rel.filter(medication_rel__id=medication.id)
                    if old_load.exists():
                        old_load = old_load[0]
                        old_load.quantity += load_data['quantity']
                        old_load.save()
                        flight[0].save()
                    else:
                        Load.objects.create(
                            flight_rel=flight,
                            quantity=load_data['quantity'],
                            medication_rel=medication
                        )
                    drone.save()
                    if drone.get_load_weight() == drone.weight_limit:
                        drone.state = 'LOADED'
                        drone.save()
                else:
                    return Response({'details': _('The load is higher that the current weight capacity of the drone')}, status=400)
            else:
                return Response({'details': _('The drone cannot accept new load')}, status=400)
        else:
            return Response({'details': _('Invalid payload')}, status=400)

        flights = drone.flights_rel.filter(was_delivered=False)
        loads = {}
        if flights.exists():
            loads = flights[0].loads_rel
        return Response(DroneLoadSerializer(embed=True, many=True).to_representation(loads))


    @extend_schema(methods=['get'], responses={200: DroneSerializer(many=True)},
                   description="API endpoint allowing to retrieve the available drones for loading.")
    @action(detail=False, methods=['get'])
    def available_for_loading(self, request, pk=None):
        """
        Endpoint to get the drones available for loading
        """

        drones = Drone.objects.filter(
            Q(state='IDLE', battery_capacity__gte=25) |
            Q(state='LOADING')
        )

        page = self.paginate_queryset(drones)
        if page is not None:
            return self.get_paginated_response(DroneSerializer(embed=True, many=True).to_representation(drones))

        return Response(DroneSerializer(embed=True, many=True).to_representation(drones))