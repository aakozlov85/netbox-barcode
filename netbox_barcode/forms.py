from dcim.models import Device
from netbox.forms import NetBoxModelForm
from django.forms import ModelForm, ValidationError
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import widgets

from .models import BarcodeList


class BarcodeForm(ModelForm):
    deviceitems = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        help_text="Choose a device to add in list",
    )

    class Meta:
        model = BarcodeList
        fields = ('deviceitems',)

    def save(self, *args, **kwargs):
        for device_objects in args:
            for item in device_objects:
                BarcodeList.objects.create(device=item)

    def clean_deviceitems(self):
        data = self.cleaned_data['deviceitems']
        device_in_list = Device.objects.filter(barcode_list__isnull=False)
        for item in data:
            if item in device_in_list:
                raise ValidationError(f"Device {item} allready in list. "
                                    "Please remove it and choose another one!", code="invalid_choice")
        return data

    # def __init__(self, *args, **kwargs):
    #     super(BarcodeForm, self).__init__(*args, **kwargs)
    #     self.fields['device'].initial = [c.pk for c in Device.objects.filter()]

