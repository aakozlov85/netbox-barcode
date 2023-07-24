from extras.plugins import PluginConfig


class NetBoxBarcodeConfig(PluginConfig):
    name = 'netbox_barcode'
    verbose_name = ' NetBox Barcodes'
    description = 'Barcode generation for netbox'
    version = '0.3'
    base_url = 'barcode'


config = NetBoxBarcodeConfig
