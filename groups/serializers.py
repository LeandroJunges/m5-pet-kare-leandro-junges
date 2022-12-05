from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    scienthific_name = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only = True)