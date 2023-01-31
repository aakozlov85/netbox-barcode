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