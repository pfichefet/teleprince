{
    'name': 'Task Report No Timesheets Addons',
    'version': '2.0.1',
    'summary': 'Create a new task report without the TS details.',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
Task Report No Timesheets Addons
================================
Create a new task report without the TS details.
    """,
    'category': 'Hidden',
    'depends': ['industry_fsm_report'],
    'external_dependencies': {
    },
    'data': [
        # Reports
        'report/worksheet_custom_report.xml',
        'report/worksheet_custom_report_templates.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
