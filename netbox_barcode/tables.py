import django_tables2 as tables
from netbox.tables import NetBoxTable
from dcim.models import Device
import itertools


class BarcodeTable(NetBoxTable):
    counter = tables.Column(verbose_name='#', empty_values=(), orderable=False)
    name = tables.Column(
        linkify=True,
        orderable=False
    )
    serial = tables.Column(orderable=False)
    device_type = tables.Column(orderable=False)
    partnumber = tables.Column(accessor='device_type.part_number',
                               orderable=False
                               )
    actions = tables.TemplateColumn(verbose_name='Action',
                                    template_name='netbox_barcode/table_actions.html', orderable=False)

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ('counter', 'name', 'serial', 'device_type', 'partnumber')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return next(self.row_counter)+1
