
{
    "name": "Stock Request",
    "summary": "Internal request for stock",
    "version": "13.0.1.3.0",
    "license": "LGPL-3",
    "category": "Warehouse Management",
    "depends": ["stock"],
    "data": [
        "security/stock_request_security.xml",
        "security/ir.model.access.csv",
        "views/stock_request_views.xml",
        "views/stock_request_menu.xml",
        "data/stock_request_sequence_data.xml",
        'report/stock_request_orders_report.xml',
    ],
    "installable": True,
}
