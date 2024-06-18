# -*- coding: utf-8 -*-
{
    'name': "Sale Inventory Api",

    'summary': """
   """,
    'category': 'Sale',

    'version': '16.0.1.0.12',

    'depends': ['base', 'sale', 'sale_stock', 'stock'],

    'data': [
        'data/cron.xml',
        'views/sale.xml',
        'views/res_company.xml',
        'views/stock_quant.xml',
    ],
    'license': 'LGPL-3',
}
