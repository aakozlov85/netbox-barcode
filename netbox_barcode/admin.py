from django.contrib import admin
from .models import (BarcodeSnDevice,
                     BarcodeStockDevice,
                     BarcodePartNumber
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
class deviceStockAdmin(admin.ModelAdmin):
    def device_type(self, obj):
        return obj.device_type.model
    readonly_fields = ('barcode', 'image_tag')
    list_display = ('pk', 'device_type', 'part_number', 'barcode')
    search_fields = ('part_number',)
