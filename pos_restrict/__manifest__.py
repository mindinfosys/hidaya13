# -*- coding: utf-8 -*-
{
    'name': 'POS Session Restrict',
    'summary': """Restricts User access to pos and orders""",
    'version': '13.0.1.0.0',
    'description': """Restricts User session access to pos and orders""",
    'author': 'Sananaz Mansuri',
    'company': 'mindinfosys.com',
    'website': 'https://mindinfosys.com',
    'category': 'Tools',
    'depends': ['point_of_sale'],
    'data': [
        'security/security.xml',
        'views/res_users_inherit.xml'
    ],
    'images': [],
    'installable': True,
    'auto_install': False,
}
