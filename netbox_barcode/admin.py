from django.contrib import admin
from .models import (BarcodeSnDevice,
                     BarcodeStockDevice,
                     BarcodePartNumber,
                     BarcodeList,
                     )


@admin.register(BarcodeSnDevice)
class deviceSnAdmin(admin.ModelAdmin):
    def name(self, obj):
        return obj.device.name
    readonly_fields = ('barcode', 'image_tag')
    list_display = ('pk', 'name', 'sn', 'barcode')
    search_fields = ('sn',)


@admin.register(BarcodeStockDevice)
class deviceStockAdmin(admin.ModelAdmin):
    def name(self, obj):
        return obj.device.name
    readonly_fields = ('barcode', 'image_tag')
    list_display = ('pk', 'name', 'stock_number', 'barcode')
    search_fields = ('stock_number',)


@admin.register(BarcodePartNumber)
class devicePartAdmin(admin.ModelAdmin):
    def device_type(self, obj):
        return obj.device_type.model
    readonly_fields = ('barcode', 'image_tag')
    list_display = ('pk', 'device_type', 'part_number', 'barcode')
    search_fields = ('part_number',)

@admin.register(BarcodeList)
class deviceListAdmin(admin.ModelAdmin):
    def device_type(self, obj):
        return obj.device.device_type.model
    def serial_number(self, obj):
        return obj.device.serial
    list_display = ('pk', 'serial_number', 'device_type')