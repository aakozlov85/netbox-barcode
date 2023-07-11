import django_tables2 as tables
from netbox.tables import NetBoxTable
from dcim.models import Device


class BarcodeTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    serial = tables.Column()
    device_type = tables.Column()
    actions = tables.TemplateColumn(verbose_name='Action',
                                    template_name='netbox_barcode/table_actions.html', orderable=False)

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ('name', 'serial', 'device_type')
