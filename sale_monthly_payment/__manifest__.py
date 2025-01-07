{
    'name': 'Sale Monthly Financing Payment',
    'version': '1.0.0',
    'summary': 'Add a field to indicate the monthly payment of the financing.',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
Sale Monthly Financing Payment
==============================
On sale order a new flag indicate whether this order have a financing.
If it does the monthly payment can be encoded on the sale order.

The monhtly payment appears on the PDF report and also on the portal view of the sale order.
    """,
    'category': 'Sales/Sales',
    'depends': ['sale'],
    'external_dependencies': {
    },
    'data': [
        # Reports
        'report/sale_order_reports.xml',
        # Views
        'views/sale_order_views.xml',
        'views/sale_portal_templates.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
