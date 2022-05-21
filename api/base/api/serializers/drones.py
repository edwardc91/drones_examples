from base.models import Drone
from dynamic_rest.serializers import DynamicModelSerializer


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
