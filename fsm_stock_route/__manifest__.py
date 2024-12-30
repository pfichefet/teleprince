{
    'name': 'FSM Stock Route',
    'version': '2.0.1',
    'summary': 'Sale Order Line created from an FSM task use a specific route.',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
FSM Stock Route
===============
In the settings of the project you can sepcify a logistic route to be used..
    """,
    'category': 'Services/Field Service',
    'depends': ['industry_fsm_sale'],
    'external_dependencies': {
    },
    'data': [
        # Views
        'views/stock_warehouse_views.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
