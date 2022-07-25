# -*- coding: utf-8 -*-
{
    "name": "Sale Purchase Inventory Extends",
    "summary": "Sale Purchase Inventory Extends",
    "version": "1.0.0",
    "license": "Other proprietary",
    'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    "category": "Sale, Stock",
    "depends": [
        "sale",
        "stock",
        "purchase",
    ],
    "data": [
        'security/security.xml',
        'data/purchase_email_template.xml',
        'views/sale_order_view.xml',
        'views/stock_view.xml',
    ],
    "installable": True,
}
