from extras.plugins import PluginTemplateExtension
from django.urls import reverse

from .models import BarcodeList


class NetcubeBarcode(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        object = self.context['object']
        object_in_list = BarcodeList.objects.filter(device=object.id).exists()
        object_url = reverse(
            'plugins:netbox_barcode:barcode_info', args=[object.id])
        object_url_changelist = reverse(
            'plugins:netbox_barcode:barcode_change_list', args=[object.id])
        return self.render('netbox_barcode/barcode.html', extra_context={'object_url': object_url,
                                                                         'object_in_list': object_in_list,
                                                                         'object_url_changelist': object_url_changelist})


template_extensions = [NetcubeBarcode]
