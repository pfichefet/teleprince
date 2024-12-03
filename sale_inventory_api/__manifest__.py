{
    'name': 'B&O Rest API',
    'version': '1.0',
    'summary': 'Sent sale and inventory report to B&O through REST API',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
B&O Rest API
============
Sent sale and inventory report to B&O through REST API.
    """,
    'category': 'Sales/Sales',
    'depends': ['sale', 'stock', 'uom', 'purchase', 'pos_sale'],
    'external_dependencies': {
    },
    'data': [
        # Data
        'data/bo_report_type.xml',
        'data/ir_cron.xml',
        'data/ir_sequence.xml',
        # Security
        'security/b_and_o_api_security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/res_config_settings_views.xml',
        'views/bo_report_type_views.xml',
        'views/bo_report_views.xml',
        'views/stock_warehouse_views.xml',
        'views/stock_quant_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/menu.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
