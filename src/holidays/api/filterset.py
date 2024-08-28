from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
from djgentelella.fields.drfdatetime import DateRangeTextWidget

from holidays.models import Holiday


class HolidayFilter(FilterSet):

    date = DateFromToRangeFilter(
        widget=DateRangeTextWidget(attrs={'planeholder': 'YYYY/MM/DD'})
    )

    class Meta:
        model = Holiday
        fields = {'id': ['exact'],
                  'name': ['icontains'],
                  'country': ['icontains']
                  }