FROM python:3.10

ARG netbox_ver=v4.1.5

RUN pip install --upgrade pip

# -------------------------------------------------------------------------------------
# Install NetBox
# -------------------------------------------------------------------------------------
# WORKDIR /opt/netbox
# COPY /netbox /opt/netbox

# RUN pip install -r /opt/netbox/requirements.txt
RUN git clone --single-branch --branch ${netbox_ver} https://github.com/netbox-community/netbox.git /opt/netbox/ && \
    cd /opt/netbox/ && \
    pip install -r /opt/netbox/requirements.txt

# Work around https://github.com/rq/django-rq/issues/421
# RUN pip install django-rq==2.3.2

# -------------------------------------------------------------------------------------
# Install Netbox Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /netbox-barcode
WORKDIR /netbox-barcode
COPY ./setup.py /netbox-barcode
COPY ./MANIFEST.in /netbox-barcode
COPY ./requirements_barcode.txt /netbox-barcode

RUN pip install -r requirements_barcode.txt
RUN python setup.py develop

WORKDIR /opt/netbox/netbox/
