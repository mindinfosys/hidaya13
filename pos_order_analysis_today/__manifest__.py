# -*- coding: utf-8 -*-

# Part of Sananaz Mansuri See LICENSE file for full copyright and licensing details.

{

    'name': 'POS Order Analysis Today',
    'version': '1.0.0',
    'category': "Point of Sale",
    'summary': 'POS Order Analysis Today.',
    'description': """
        - POS Order Analysis Today
        
            """,
    'author': 'Sananaz Mansuri',
    'website': 'www.odoo.com',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/pos_analysis_view.xml',
     ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
