{
    "name": "Project Task Addons",
    "version": "2.0.1",
    "summary": "Addons to the project task workflow.",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    "description": """
Project Task Addons
====================
- Add start date and end date on kanban view.
- Allow to add date from the quick task create.
- Allow to link a sale order line from a different partner on a task.
- Allow to assign a secondary partner on a field service task.
    """,
    "category": "Hidden",
    "depends": ["industry_fsm_sale"],
    "external_dependencies": {},
    "data": [
        # Views
        "views/project_task_views.xml",
    ],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
