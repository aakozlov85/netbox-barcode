from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('netbox_barcode/<int:pk>/', views.DeviceBarcodeIdView.as_view(),
         name='barcode_info'),
    path('netbox_barcode/<int:pk>/changelist', views.DeviceBarcodePrintAddRemoveView.as_view(),
         name='barcode_change_list'),
    path('netbox_barcode/bulkprint', views.DeviceBarcodePrintView.as_view(),
         name='barcode_bulkprint'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
