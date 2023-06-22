from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
# from django.http import HttpResponse
from dcim.models import Device, DeviceType

# from .forms import BarcodeForm
from .models import BarcodeSnDevice, BarcodeStockDevice, BarcodePartNumber, BarcodeList
from .utils import count_device_with_bays

from django.utils.decorators import method_decorator
from django.views.decorators.cache import patch_cache_control
from functools import wraps

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
                    BarcodePartNumber.objects.get(device_type=devicetype).save()
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

def never_ever_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-axe=0 Firefox returns cached results
    of GET calls when it is restarted.
    """
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response
    return wrapper


class DeviceBarcodePrintView(View):
    # class for bulk print barcodes
    devices = Device.objects.filter(barcode_list__isnull=False)
    # queryset = BarcodeList.objects.all()
    template_name = 'netbox_barcode/barcode_bulkprint.html'
    
    @method_decorator(never_ever_cache)
    def get(self, request):
        return render(
                request, self.template_name, {"devices": self.devices,}
            )
            



class DeviceBarcodePrintAddRemoveView(View):
    # class for bulk add or remove barcodes list from device page
    
    def post(self, request, pk):
        device = get_object_or_404(Device, id=pk)
        if request.POST['editlist'] == 'add':
            BarcodeList.objects.get_or_create(device=device)
        elif request.POST['editlist'] == 'remove':
            BarcodeList.objects.filter(device=device).delete()
        return redirect(device.get_absolute_url())

