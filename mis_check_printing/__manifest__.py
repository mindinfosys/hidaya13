# -*- coding: utf-8 -*-
{
    'name': 'MIS Checks Layout',
    'version': '13.0.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Print AE Checks',
    'description': """
This module allows to print your payments on pre-printed check paper.

    """,
    'website': 'http://www.mindinfosys.com',
    'depends' : ['account_check_printing'],
    'data': [
        'data/mis_check_printing.xml',
        'wizard/print_prenumbered_checks_views.xml',
        'views/account_payment.xml',
        'report/print_check_layout1.xml',
        'report/print_check_layout2.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
