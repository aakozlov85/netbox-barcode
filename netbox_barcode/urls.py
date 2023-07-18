from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path('netbox_barcode/<int:pk>/', views.DeviceBarcodeIdView.as_view(),
         name='barcode_info'),
    path('netbox_barcode/<int:pk>/changelist', views.DeviceBarcodePrintAddRemoveView.as_view(),
         name='barcode_change_list'),
    path('netbox_barcode/bulkprint_table', views.DeviceBarcodeBulkTableView.as_view(),
         name='barcode_bulktable'),
    path('netbox_barcode/addform', views.DeviceBarcodeTableAddView.as_view(),
         name='barcode_addform'),
#     path('netbox_barcode/barcode_info_bulk/', views.DeviceBarcodePrintView.as_view(),
#          name='barcode_bulkprint'),
]
