from setuptools import find_packages, setup

setup(
    name='netbox-barcode',
    version='0.3',
    description='barcode plugin for netbox devices',
    author='Andrey Kozlov',
    author_email='kozlov@netcube.ru',
    install_requires=[
        'python-barcode',
        'Pillow',
        'requests',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
