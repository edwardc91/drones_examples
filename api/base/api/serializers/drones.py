from base.models import Drone, Load

from dynamic_rest.fields.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from base.api.serializers.medications import MedicationSerializer


class DroneSerializer(DynamicModelSerializer):

    class Meta:
        model = Drone
        ref_name = 'Drone'
        name = 'drone'
        view_name = 'drones-list'
        fields = ('pk', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state')


class DroneBatterySerializer(DynamicModelSerializer):

    class Meta:
        model = Drone
        ref_name = 'Drone'
        name = 'drone'
        view_name = 'drones-list'
        fields = ('pk', 'battery_capacity',)


class DroneLoadSerializer(DynamicModelSerializer):
    class Meta:
        model = Load
        ref_name = 'Load'
        name = 'Load'
        view_name = 'Loads-list'
        fields = ('pk', 'medication_rel', 'quantity')

    medication_rel = DynamicRelationField(MedicationSerializer)