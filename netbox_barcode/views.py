from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from dcim.models import Device, DeviceType

from .models import BarcodeSnDevice, BarcodeStockDevice, BarcodePartNumber


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
                      })

