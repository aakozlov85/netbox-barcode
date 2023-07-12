from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View
from dcim.models import Device, DeviceType
# from netbox.views import generic

from .models import BarcodeSnDevice, BarcodeStockDevice, BarcodePartNumber, BarcodeList
from .utils import count_device_with_bays
from .tables import BarcodeTable
from .forms import BarcodeForm


class DeviceBarcodeIdView(View):
    template_name = 'netbox_barcode/barcode_info.html'

    def get(self, request, pk):
        device = get_object_or_404(Device, id=pk)
        devicetype = device.device_type
        sn = device.serial
        stocknumber = device.custom_field_data.get('Stock_number')
        partnumber = devicetype.part_number
        barcode_sn = None
        barcode_stocknumber = None
        barcode_partnumber = None
        if sn != '':
            try:
                barcode_object = device.barcode_sn
                # check if sn was changed in device model
                if barcode_object.sn == sn:
                    barcode_sn = barcode_object.barcode
                else:
                    BarcodeSnDevice.objects.filter(device=device).update(sn=sn)
                    BarcodeSnDevice.objects.get(device=device).save()
                    barcode_sn = BarcodeSnDevice.objects.get(
                        device=device).barcode
            except Device.barcode_sn.RelatedObjectDoesNotExist:
                barcode_object = BarcodeSnDevice.objects.create(
                    device=device, sn=sn)
                barcode_sn = device.barcode_sn.barcode
        if stocknumber != None:
            try:
                barcodestock_object = device.barcode_stock
                # check if stock number was changed in device model
                if barcodestock_object.stock_number == stocknumber:
                    barcode_stocknumber = barcodestock_object.barcode
                else:
                    BarcodeStockDevice.objects.filter(
                        device=device).update(stock_number=stocknumber)
                    BarcodeStockDevice.objects.get(device=device).save()
                    barcode_stocknumber = BarcodeStockDevice.objects.get(
                        device=device).barcode
            except Device.barcode_stock.RelatedObjectDoesNotExist:
                barcodestock_object = BarcodeStockDevice.objects.create(
                    device=device, stock_number=stocknumber)
                barcode_stocknumber = device.barcode_stock.barcode
        if partnumber != '':
            try:
                barcodepn_object = devicetype.barcode_pn
                # check if stock number was changed in device model
                if barcodepn_object.part_number == partnumber:
                    barcode_partnumber = barcodepn_object.barcode
                else:
                    BarcodePartNumber.objects.filter(
                        device_type=devicetype).update(part_number=partnumber)
                    BarcodePartNumber.objects.get(
                        device_type=devicetype).save()
                    barcode_partnumber = BarcodePartNumber.objects.get(
                        device_type=devicetype).barcode
            except DeviceType.barcode_pn.RelatedObjectDoesNotExist:
                barcodepn_object = BarcodePartNumber.objects.create(
                    device_type=devicetype, part_number=partnumber)
                barcode_partnumber = devicetype.barcode_pn.barcode
        return render(request, self.template_name,
                      {
                          'sn': sn,
                          'barcode_sn': barcode_sn,
                          'stock_number': stocknumber,
                          'barcode_stocknumber': barcode_stocknumber,
                          'partnumber': partnumber,
                          'barcode_partnumber': barcode_partnumber,
                          'device_count': count_device_with_bays(device),
                      })


class DeviceBarcodePrintView(View):
    # class for bulk print barcodes
    devices = Device.objects.filter(barcode_list__isnull=False)
    template_name = 'netbox_barcode/barcode_bulkprint.html'

    def get(self, request):
        table = BarcodeTable(self.devices)
        table.configure(request)
        return render(
            request, self.template_name, {"table_barcode": table}
        )

    def post(self, request):
        if request.POST['editlist'] == 'removeall':
            BarcodeList.objects.all().delete()
            return redirect(reverse('plugins:netbox_barcode:barcode_bulkprint'))


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
            return redirect(reverse('plugins:netbox_barcode:barcode_bulkprint'))
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
            device = form.cleaned_data['device']
            form.save()
            return redirect(reverse('plugins:netbox_barcode:barcode_bulkprint'))
        return render(
            request, self.template_name, {"form": form}
        )
