# -*- coding: utf-8 -*-
{
    'name': "SO Line Invoice Create",
    'version': '2.1.0',
    'license': 'Other proprietary',
    'category': 'Invoicing Management',
    'summary': """SO Line Invoice Create""",
    'description': """
        SO Line Invoice Create.
    """,
    'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    'live_test_url': '',
    'depends': [
        'sale',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/source_location_view.xml',
        'views/stock_view.xml',
        'wizard/create_so_inv_view.xml',
    ],
    'installable': True,
    'application': False,
}
