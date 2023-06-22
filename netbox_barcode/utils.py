from barcode import Gs1_128
from io import BytesIO
from barcode.writer import ImageWriter

CODE_QUALITY = {
    'font_size': 0,
    'quiet_zone': 2.0,
    'module_height': 9.0,
    'text_distance': 5.0,
    'dpi': 260,
}

def get_barcode(data):
    barcode = Gs1_128(data, ImageWriter())
    buffer = BytesIO()
    barcode.write(buffer, CODE_QUALITY)
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