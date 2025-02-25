{
    'name': "Add Payment Method On the Invoice",
    'version': '1.0.0',
    'summary': """ For invoices generated from the point of sale display the payment method. """,
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """

    """,
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    'external_dependencies': {
    },
    'data': [
        # Views
        'views/report_invoice.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
