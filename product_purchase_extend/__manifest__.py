# -*- coding: utf-8 -*-

{
    "name": "Stock Request Multi Company",
    "summary": "Internal request for stock",
    "version": "3.0.0",
    "license": "Other proprietary",
'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    "category": "Warehouse Management",
    "depends": [
        "purchase",
    ],
    "data": [
        'views/product_views.xml',
        'wizard/create_po_views.xml',
    ],
    "installable": True,
}
