from django import forms
from djgentelella.widgets import core as genwidgets
from djgentelella.forms.forms import GTForm

from holidays.models import Holiday


class HolidayForm(GTForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        modal_id = kwargs.pop('modal_id')
        super(HolidayForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Holiday
        fields = "__all__"
        widgets = {
            "name": genwidgets.TextInput,
            "country": genwidgets.TextInput,
            "date": genwidgets.DateInput
        }