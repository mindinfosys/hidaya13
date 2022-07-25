# -*- coding: utf-8 -*-
{
    'name': "Credit Debit Note Picking",
    'version': '1.0.0',
    'license': 'Other proprietary',
    'category': 'Invoicing Management',
    'summary': """Credit Debit Note Picking""",
    'description': """
        Credit Debit Note Picking
    """,
    'author': "Sananaz Mansuri",
    'website': 'www.odoo.com',
    'live_test_url': '',
    'depends': [
        'stock',
        'account',
        'purchase',
    ],
    'data': [
        'wizard/stock_return_picking_view.xml',
    ],
    'installable': True,
    'application': False,
}
