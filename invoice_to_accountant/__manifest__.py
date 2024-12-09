# -*- coding: utf-8 -*-
{
    'name': 'Send Invoices to Accountant',
    'version': '2.0.1',
    'summary': 'Send invoices to accountant by email',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
Send Invoices to Accountant
===========================
Send invoices to accountant by email.
    """,
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    'external_dependencies': {
    },
    'data': [
        # Views
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
