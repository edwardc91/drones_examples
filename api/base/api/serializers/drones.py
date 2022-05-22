from django.utils.translation import ugettext_lazy as _

from dynamic_rest.fields.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from rest_framework import serializers

from base.models import Drone, Load
from base.api.serializers.medications import MedicationSerializer


class DroneSerializer(DynamicModelSerializer):

    class Meta:
        model = Drone
        ref_name = 'Drone'
        name = 'drone'
        view_name = 'drones-list'
        fields = ('pk', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state')

    def validate_weight_limit(self, value):
        """
        Check that the weight limit is greater than 0 and less or equal than 500
        """

        if value <= 0 or value > 500:
            raise serializers.ValidationError(_("Weight limit must be greater than 0 and less or equal than 500."))
        return value

    def validate_battery_capacity(self, value):
        """
        Check that the battery capacity is greater than 0 and less or equal than 100
        """

        if value < 0 or value > 100:
            raise serializers.ValidationError(_("Battery capacity must be greater or equal than 0 and less or equal than 100."))
        return value


class DroneBatterySerializer(DynamicModelSerializer):

    class Meta:
        model = Drone
        ref_name = 'DroneBattery'
        name = 'dronebattery'
        view_name = 'dronebatteries-list'
        fields = ('pk', 'battery_capacity',)


class DroneLoadSerializer(DynamicModelSerializer):
    class Meta:
        model = Load
        ref_name = 'Load'
        name = 'Load'
        view_name = 'Loads-list'
        fields = ('pk', 'medication_rel', 'quantity')

    medication_rel = DynamicRelationField(MedicationSerializer)

class DroneCurrentLoadSerializer(serializers.Serializer):

    current_load = serializers.FloatField()

class DroneAddLoadSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    medication = serializers.IntegerField()