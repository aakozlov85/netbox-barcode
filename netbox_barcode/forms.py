from dcim.models import Device
from django.forms import ModelForm, ValidationError
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField 

from .models import BarcodeList


class BarcodeForm(ModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        help_text="Choose a device to add in list",
    )

    class Meta:
        model = BarcodeList
        fields = ('device',)

    def clean_device(self):
        device = self.cleaned_data['device']
        device_in_list = Device.objects.filter(barcode_list__isnull=False)
        if device in device_in_list:
            raise ValidationError("This device allready in list. "
                                  "Please choose another one!", code="invalid")
        return device
