{
    'name': "Invoice Templates",
    'version': '1.0.0',
    'summary': """ Logo Based on the template selected on invoice """,
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """

    """,
    'category': 'Accounting/Accounting',
    'depends': ['base', 'account', 'web', 'base_setup', 'sale_margin'],
    'external_dependencies': {
    },
    'data': [
        # Security
        'security/security.xml',
        # Report
        'reports/invoice_doc.xml',
        # Views
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
        'views/res_company_views.xml',
        'views/res_config_views.xml',
        'views/report_templates.xml',
        'views/product_template_views.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
