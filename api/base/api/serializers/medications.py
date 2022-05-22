from django.utils.translation import ugettext_lazy as _

from dynamic_rest.serializers import DynamicModelSerializer

from rest_framework import serializers

from base.models import Medication

import re


class MedicationSerializer(DynamicModelSerializer):

    class Meta:
        model = Medication
        ref_name = 'Medication'
        name = 'medication'
        view_name = 'medications-list'
        fields = ('pk', 'name', 'weight', 'code', 'image',)

    def validate_code(self, value):
        """
        Check that the code only have A-Z,-, or _
        """

        reg = re.compile('([A-Z0-9]|-|_)+')
        if not reg.fullmatch(value) :
            raise serializers.ValidationError(_("Invalid code value."))
        return value

    def validate_weight(self, value):
        """
        Check that the weight is greater than 0
        """

        if value <= 0 or value > 500:
            raise serializers.ValidationError(_("Weight must be greater than 0 and less than 500."))
        return value