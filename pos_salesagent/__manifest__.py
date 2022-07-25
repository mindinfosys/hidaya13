{
    'name': 'POS Sales Agent Commission',
    'summary': """Allows Sales Agent selection from pos interface and
    			provides report for sales agent commission""",
    'version': '13.0.1.0.0',
    'description': """Allows Sales Agent selection from pos interface and
    			provides report for sales agent commission""",
    'author': 'Mindinfosys FZE LLC',
    'company': 'Mindinfosys FZE LLC',
    'website': 'http://www.mindinfosys.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale', 'hr'],
    'license': 'AGPL-3',
    'data': [
        'views/pos_employee_template.xml',
        'views/hr_employee_view_inherited.xml',
        'views/pos_order_agent_inherited.xml',
        'views/pos_config_inherited_view.xml',
        'views/product_template.xml',
        'wizard/agent_commission_wizard_view.xml',
    ],
    'qweb': ['static/src/xml/pos_agent_selection.xml'],
#    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,

}
