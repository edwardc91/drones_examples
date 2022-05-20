from base.models import Medication
from dynamic_rest.serializers import DynamicModelSerializer


class MedicationSerializer(DynamicModelSerializer):

    class Meta:
        model = Medication
        ref_name = 'Medication'
        name = 'medication'
        view_name = 'medications-list'
        fields = ('pk', 'name', 'weight', 'code', 'image',)