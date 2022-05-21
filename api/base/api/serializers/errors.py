from rest_framework import serializers

class ErrorSerializer(serializers.Serializer):
    details = serializers.CharField(help_text="Error details")

class SuccessSerializer(serializers.Serializer):
    details = serializers.CharField(help_text="Success details")