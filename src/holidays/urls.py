from django.urls import path, include
from rest_framework.routers import DefaultRouter

from holidays.api.views import HolidayManagementViewset
from holidays.views import get_api, holiday_list, index_holidays

app_name = 'holiday'
objectrouter = DefaultRouter()
objectrouter.register('api_holiday_list', HolidayManagementViewset, basename='api-holiday')

urlpatterns = [
    path('', index_holidays, name="index"),
    path('list/', holiday_list, name="holiday_list"),
    path('api/', include(objectrouter.urls)),


    # TEST
    path('verAPI', get_api, name="consumoApi"),
]
