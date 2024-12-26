{
    'name': 'Repair Order Location',
    'version': '2.0.1',
    'summary': 'Allow to create location for repair orders.',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
Repair Order Locations
===================
Allow to create locations for repair orders.
    """,
    'category': 'Inventory/Inventory',
    'depends': ['repair'],
    'external_dependencies': {
    },
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/repair_order_location_views.xml',
        'views/repair_order_views.xml',

    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
