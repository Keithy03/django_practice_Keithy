import requests
from django.shortcuts import render
from rest_framework.views import APIView

from holidays.api.serializers import HolidayDataTableSerializer
from holidays.form import HolidayForm
from holidays.models import Holiday


def index_holidays(request):
    holidays = Holiday.objects.all()
    return render(request, "holidays/holidays_list.html", {'holidays': holidays})

def holiday_list(request):
    create_form = HolidayForm(prefix="create", modal_id="create_obj_modal")
    update_form = HolidayForm(prefix="update", modal_id="update_obj_modal")
    return render(request, "holidays/holidays_list.html", {"create_form": create_form, "update_form": update_form})




# Consume and load (it is a test)
def get_api(request):
    url = "https://date.nager.at/api/v2/publicholidays/2023/CR"

    try:
        response = requests.get(url)
        holidays_data = response.json()

    except requests.RequestException as e:
        # Error handling.
        print(f"Error en la solicitud: {e}")
        holidays_data = []

    return render(request, "holidays/api_holidays_list.html", {'holidays_data': holidays_data})

