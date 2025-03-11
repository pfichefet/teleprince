{
    "name": "Project task and calendar event",
    "category": "Human Resources/Employees",
    "summary": "Synchronize project task and calendar event",
    "version": "1.0",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    # 'images': ['static/description/portal_employee.png'],
    "description": """
        Allow to link a calendar event to an existing project.
        When we do so a task is created within the project and linked to the calendar event.

        If we modify the event the task is updated accordingly. The other way around is also true.
        """,
    "depends": [
        "hr",
        "project",
    ],
    "qweb": [],
    "data": [
        "views/calendar_event_views.xml",
    ],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
