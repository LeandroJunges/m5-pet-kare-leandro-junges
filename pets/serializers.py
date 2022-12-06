from rest_framework import serializers
from pets.models import Sex,Pet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from groups.models import Group
from traits.models import Trait


class PetSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices= Sex.choices, default= Sex.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many = True)
    traits_count = serializers.SerializerMethodField()


    def get_traits_count(self, obj):

        traits = obj.traits.count()
        traits_count = traits
        return traits_count

    def create(self, validated_data:dict)->Pet:
        group_dict = validated_data.pop("group")
        traits_dict = validated_data.pop("traits")

        group_obj, _ = Group.objects.get_or_create(**group_dict )
        
        pet_obj = Pet.objects.create(**validated_data, group=group_obj)

        for trait_key in traits_dict:
            trait, _ = Trait.objects.get_or_create(**trait_key)
            pet_obj.traits.add(trait)

        pet_obj.save()

        return pet_obj

    def update(self, instance, validated_data:dict):
        new_traits = []
        group_dict = validated_data.pop("group", None)
        trait_dict = validated_data.pop("traits", None)
        
        if group_dict : 
            group_obj, _ = Group.objects.get_or_create(**group_dict)
            instance.group = group_obj

        if trait_dict:
            for trait in trait_dict :
                trait_obj, _ = Trait.objects.get_or_create(**trait)
                new_traits.append(trait_obj)

            instance.traits.set(new_traits)
            
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        
        return instance