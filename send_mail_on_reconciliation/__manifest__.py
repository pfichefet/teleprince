{
    'name': 'Send Email Automatically on Reconciliation',
    'version': '1.0.0',
    'summary': 'Send Email Automatically on Reconciliation',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
Send Email Automatically on Reconciliation
==========================================
In the settings of the accounting module, you can enable automatic email notifications for invoice reconciliation. 
Each invoice includes a flag that is configured based on the company's settings. 
When the flag is set to True, an email is automatically sent to the customer upon the reconciliation of the invoice.
    """,
    'category': 'Accounting/Accounting',
    'depends': ['account', 'point_of_sale'],
    'external_dependencies': {
    },
    'data': [
        # Data
        'data/mail_template_data.xml',
        # Views
        'views/res_config_settings_views.xml',
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
