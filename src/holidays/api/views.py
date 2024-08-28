from django_filters.rest_framework import DjangoFilterBackend
from djgentelella.objectmanagement import AuthAllPermBaseObjectManagement
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission

from holidays.models import Holiday
from holidays.api import serializers, filterset


class HolidayManagementViewset(AuthAllPermBaseObjectManagement):
    serializer_class = {
        'list': serializers.HolidayDataTableSerializer,
        'destroy': serializers.HolidaySerializer,
        'create': serializers.HolidaySerializer,
        'update': serializers.HolidaySerializer
    }
    perms = {
        'list': ["holiday.view_holiday"],
        'create': ["holiday.add_holiday"],
        'update': ["holiday.change_holiday"],
        'destroy': ["holiday.delete_holiday"]
    }

    permission_classes = (BasePermission,)

    queryset = Holiday.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['name', 'country']  # for the global search
    filterset_class = filterset.HolidayFilter
    ordering_fields = ['name']
    ordering = ('date',)
