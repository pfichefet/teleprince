# -*- coding: utf-8 -*-
{
    'name': "Invoice Templates",
    'summary': """ Logo Based on the template selected on invoice """,
    'category': 'account',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'web', 'base_setup', 'sale_margin'],
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
        'views/res_company_views.xml',
        'views/res_config_views.xml',
        'views/templates.xml',
        'views/product.xml',
    ],
}
