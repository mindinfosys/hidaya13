
{
    'name': 'Point of Sale Custom',
    'version': '1.0.1',
    'category': 'Sales/Point Of Sale',
    'sequence': 20,
    'summary': 'POS Report',
    'description': "",
    'depends': ['point_of_sale'],
    'data': [
        'report/report_saleclosingreport.xml',
        'report/report_menu.xml',
#         'wizard/cus_pos_details.xml',
#        'views/point_of_sale_template.xml',
#        'views/point_of_sale_report.xml',
#        'views/pos_order_report_view.xml',
#        'views/report_saleclosingreport.xml',
#        'views/report_saledetails.xml',
    ],
    'installable': True,
    'application': True,

}
