from rest_framework import serializers

from earth.models import HoldingVocher, Store, Vocher
from human.serializers import RelationshipSerializer


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class VocherSerializer(serializers.ModelSerializer):
    store = StoreSerializer(required=True)

    class Meta:
        model = Vocher
        fields = '__all__'


class HoldingVocherSerializer(serializers.ModelSerializer):
    vocher = VocherSerializer(required=True)

    class Meta:
        model = HoldingVocher
        fields = '__all__'


class UseVocherSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoldingVocher
        fields = ('label',)
