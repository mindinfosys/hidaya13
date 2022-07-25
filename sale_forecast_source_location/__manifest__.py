# -*- coding: utf-8 -*-

{
    "name": "Sale Forecast Source Location",
    "summary": "Sale Forecast Source Location",
    "version": "1.0.0",
    "license": "Other proprietary",
    'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    "category": "Sale, Stock",
    "depends": [
        "sale_stock",
        "so_line_invoice_create",
    ],
    "data": [
    ],
    'qweb': [
        'static/src/xml/qty_at_date.xml'
    ],
    "installable": True,
}
