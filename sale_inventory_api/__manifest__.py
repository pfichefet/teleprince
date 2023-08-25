# -*- coding: utf-8 -*-
{
    'name': "Sale Inventory Api",

    'summary': """
   """,
    'category': 'Sale',
    'version': '16.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'sale_management', 'account_accountant'],

    'data': [
        # 'security/ir.model.access.csv',
        'data/cron.xml',
        'views/sale.xml',
    ],
    'license': 'LGPL-3',
}
