from djgentelella.serializers import GTDateField
from rest_framework import serializers
from holidays.models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name

    def get_actions(self, obj):
        return {
            "create": True,
            "upate": True,
            "destroy": True,
            "detail": True
        }

    class Meta:
        model = Holiday
        fields = ['id', 'name', 'date', 'country', 'actions']

class HolidayDataTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=HolidaySerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)