{
    "name": "Sales Addons",
    "version": "1.0.0",
    "summary": "Brings improvements to the sale order application.",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    "description": """
Sales Addons
============
- Add the total tax included at the end of a sale order line.
    """,
    "category": "Sales/Sales",
    "depends": ["sale"],
    "external_dependencies": {},
    "data": [
        # Views
        "views/sale_order_line.xml",
    ],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
