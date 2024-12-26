{
    'name': 'CRM pre-visit Task',
    'version': '2.0.1',
    'summary': 'Allow to create a pre-visit task that is linked to an opportunity',
    'sequence': 10,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'description': """
CRM pre-visit Task
==================
Allow to create a pre-visit task that is linked to an opportunity.
    """,
    'category': 'Sales/CRM',
    'depends': ['crm', 'project_enterprise'],
    'external_dependencies': {
    },
    'data': [
        # Views
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/project_task_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
