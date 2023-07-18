from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View
from dcim.models import Device

from .models import BarcodeList
from .utils import count_device_with_bays, get_barcode_data
from .tables import BarcodeTable
from .forms import BarcodeForm


class DeviceBarcodeIdView(View):
    template_name = 'netbox_barcode/barcode_info.html'

    def get(self, request, pk):
        device_obj = get_object_or_404(Device, id=pk)
        barcode_data = get_barcode_data(device_obj)
        return render(request, self.template_name, barcode_data)


class DeviceBarcodeBulkTableView(View):
    # class for bulk print barcodes
    devices = Device.objects.filter(barcode_list__isnull=False)
    template_name = 'netbox_barcode/barcode_bulktable.html'

    def get(self, request):
        table = BarcodeTable(self.devices)
        table.configure(request)
        return render(
            request, self.template_name, {"table_barcode": table}
        )

    def post(self, request):
        if request.POST['editlist'] == 'removeall':
            BarcodeList.objects.all().delete()
            return redirect(reverse('plugins:netbox_barcode:barcode_bulktable'))


class DeviceBarcodePrintAddRemoveView(View):
    # class for add or remove barcodes list items

    def post(self, request, pk):
        device = get_object_or_404(Device, id=pk)
        if request.POST['editlist'] == 'add':
            BarcodeList.objects.get_or_create(device=device)
        elif request.POST['editlist'] == 'remove':
            BarcodeList.objects.filter(device=device).delete()
        elif request.POST['editlist'] == 'removefromtable':
            BarcodeList.objects.filter(device=device).delete()
            return redirect(reverse('plugins:netbox_barcode:barcode_bulktable'))
        return redirect(device.get_absolute_url())


class DeviceBarcodeTableAddView(View):
    # class to add device to barcode bulk table form

    template_name = 'netbox_barcode/addform.html'
    form = BarcodeForm()

    def get(self, request):
        return render(
            request, self.template_name, {"form": self.form}
        )

    def post(self, request, *args, **kwargs):
        form = BarcodeForm(request.POST)
        if form.is_valid():
            deviceitems = form.cleaned_data['deviceitems']
            form.save(deviceitems)
            return redirect(reverse('plugins:netbox_barcode:barcode_bulktable'))
        return render(
            request, self.template_name, {"form": form, }
        )
