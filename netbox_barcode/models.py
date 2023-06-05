from django.core.files import File
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe

from .utils import get_barcode

class Barcode(models.Model):

    barcode = models.ImageField(
        upload_to='image-attachments/barcodes/', blank=True, unique=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width=auto height="150" />' % (self.barcode))
    image_tag.short_description = 'Image'

    def clean(self):
        if self.barcode:
            raise ValidationError('Barcode allready exists!')

    class Meta:
        abstract = True


class BarcodeSnDevice(Barcode):
    """Model for barcode serial number."""

    device = models.OneToOneField(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name='barcode_sn',
    )
    sn = models.CharField(max_length=30,
                          blank=True,
                          null=True,
                          verbose_name='serial number',
                          )

    def save(self, *args, **kwargs):
        serialnumber = self.device.serial
        self.barcode.save(
            f'barcodesn_{serialnumber}.png', File(get_barcode(serialnumber)), save=False)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Serial Number Barcode"
        verbose_name_plural = "Serial Number Barcodes"


class BarcodeStockDevice(Barcode):
    """Model for barcode Stock number."""

    device = models.OneToOneField(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name='barcode_stock',
    )
    stock_number = models.CharField(max_length=30,
                                    blank=True,
                                    null=True
                                    )

    def save(self, *args, **kwargs):
        stocknumber = self.device.custom_field_data.get("Stock_number")
        self.barcode.save(
            f'barcodestn_{stocknumber}.png',
            File(get_barcode(stocknumber)),
            save=False
        )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock Number Barcode"
        verbose_name_plural = "Stock Number Barcodes"


class BarcodePartNumber(Barcode):
    """Model for barcode part number."""

    device_type = models.OneToOneField(
        to="dcim.DeviceType",
        on_delete=models.CASCADE,
        related_name='barcode_pn',
    )
    part_number = models.CharField(max_length=30,
                                   blank=True,
                                   null=True
                                   )

    def save(self, *args, **kwargs):
        partnumber = self.device_type.part_number
        self.barcode.save(
            f'barcodepn_{partnumber}.png',
            File(get_barcode(partnumber)),
            save=False
        )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Part Number Barcode"
        verbose_name_plural = "Part Numbers Barcodes"
