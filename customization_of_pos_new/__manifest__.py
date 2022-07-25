

{
    'name': "Customization of POS",
    'summary': """ hide the product template and add inventory xlsx report on report menu """,
    'description': """
    hide the product template and add inventory xlsx report on report menu
         """,
    'version': "13.0.1.0.0",
    'depends': [
        'base','point_of_sale','mis_xls_reports'
    ],
    'data': [
        'security/workers_groups.xml',
        'views/pos_product_template_visibility.xml'
             ],
    'qweb': [
             ],

}
