from barcode import Gs1_128
from io import BytesIO
from barcode.writer import ImageWriter
from dcim.models import Device, DeviceType

import netbox_barcode.models as md

barcode_quality = {
    'font_size': 0,
    'quiet_zone': 2.0,
    'module_height': 9.0,
    'text_distance': 5.0,
    'dpi': 260,
}


def get_barcode(data, quality = barcode_quality):
    barcode = Gs1_128(data, ImageWriter())
    buffer = BytesIO()
    barcode.write(buffer, quality)
    return buffer


def count_device_with_bays(device):
    count_parent_device = 1
    count_child_in_bays = 0

    if device.devicebays.count() != 0:
        for bay in device.devicebays.values('installed_device_id'):
            if bay.get('installed_device_id') != None:
                count_child_in_bays += 1
        return count_parent_device + count_child_in_bays
    return count_parent_device


def get_barcode_data(device):
    devicetype = device.device_type
    sn = device.serial
    stocknumber = device.custom_field_data.get('Stock_number')
    partnumber = devicetype.part_number
    barcode_sn, barcode_stocknumber, barcode_partnumber = None, None, None
    if sn != '':
        try:
            barcode_object = device.barcode_sn
            # check if sn was changed in device model
            if barcode_object.sn == sn:
                barcode_sn = barcode_object.barcode
            else:
                md.BarcodeSnDevice.objects.filter(device=device).update(sn=sn)
                md.BarcodeSnDevice.objects.get(device=device).save()
                barcode_sn = md.BarcodeSnDevice.objects.get(
                    device=device).barcode
        except Device.barcode_sn.RelatedObjectDoesNotExist:
            barcode_object = md.BarcodeSnDevice.objects.create(
                device=device, sn=sn)
            barcode_sn = device.barcode_sn.barcode
    if stocknumber != None:
        try:
            barcodestock_object = device.barcode_stock
            # check if stock number was changed in device model
            if barcodestock_object.stock_number == stocknumber:
                barcode_stocknumber = barcodestock_object.barcode
            else:
                md.BarcodeStockDevice.objects.filter(
                    device=device).update(stock_number=stocknumber)
                md.BarcodeStockDevice.objects.get(device=device).save()
                barcode_stocknumber = md.BarcodeStockDevice.objects.get(
                    device=device).barcode
        except Device.barcode_stock.RelatedObjectDoesNotExist:
            barcodestock_object = md.BarcodeStockDevice.objects.create(
                device=device,
                stock_number=stocknumber
            )
            barcode_stocknumber = device.barcode_stock.barcode
    if partnumber != '':
        try:
            barcodepn_object = devicetype.barcode_pn
            # check if stock number was changed in device model
            if barcodepn_object.part_number == partnumber:
                barcode_partnumber = barcodepn_object.barcode
            else:
                md.BarcodePartNumber.objects.filter(
                    device_type=devicetype).update(part_number=partnumber)
                md.BarcodePartNumber.objects.get(
                    device_type=devicetype).save()
                barcode_partnumber = md.BarcodePartNumber.objects.get(
                    device_type=devicetype).barcode
        except DeviceType.barcode_pn.RelatedObjectDoesNotExist:
            barcodepn_object = md.BarcodePartNumber.objects.create(
                device_type=devicetype, part_number=partnumber)
            barcode_partnumber = devicetype.barcode_pn.barcode
    return {
        'sn': sn,
        'barcode_sn': barcode_sn,
        'stock_number': stocknumber,
        'barcode_stocknumber': barcode_stocknumber,
        'partnumber': partnumber,
        'barcode_partnumber': barcode_partnumber,
        'device_count': count_device_with_bays(device),
    }

