from rest_framework import serializers
from pets.models import Sex,Pet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 10)
    age = serializers.IntegerField()
    weigth = serializers.FloatField()
    sex = serializers.ChoiceField(choices= Sex.choices, default= Sex.DEFAULT)
    group = GroupSerializer(many = True)
    trait = TraitSerializer(many = True)

    def create(self, validated_data:dict)->Pet:
        pet = Pet.objects.create(**validated_data)
        return pet

    def update(self, instance, validated_data:dict):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        
        return instance