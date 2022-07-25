# -*- coding: utf-8 -*-
{
    'name': 'MIS PDC Report',
    'version': '13.0.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'PDC Report',
    'description': """
Print PDC report.
    """,
    'website': 'http://www.mindinfosys.com',
    'depends': ['base', 'account', 'mis_check_printing'],
    'data': [
        'wizard/print_pdc_views.xml',
        'views/account_payment.xml',
        'report/pdc_report_menu.xml',
        'report/report_pdc.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
