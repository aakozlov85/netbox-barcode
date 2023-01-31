from extras.plugins import PluginTemplateExtension
from django.urls import reverse


class NetcubeBarcode(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        object = self.context['object']
        object_url = reverse(
            'plugins:netbox_barcode:barcode_info', args=[object.id])
        return self.render('netbox_barcode/barcode.html', extra_context={'object_url': object_url})


template_extensions = [NetcubeBarcode]
