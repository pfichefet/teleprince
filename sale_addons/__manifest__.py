{
    "name": "Sales Addons",
    "category": "",
    "summary": "Brings improvements to the sale order application.",
    "version": "1.0.0",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    # 'images': ['static/description/portal_employee.png'],
    "description": """
        Sales Addons
        ============
        - Add the total tax included at the end of a sale order line.
        """,
    "depends": ["sale"],
    "qweb": [],
    "data": ["views/sale_order_line.xml"],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
