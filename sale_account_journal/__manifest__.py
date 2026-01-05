{
    "name": "Sale Account Journal",
    "version": "2.0.1",
    "summary": "Set the sales journal on the warehouse to be used upon invoicing",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    "description": """
Sale Account Journal
=====================
Set the sales journal on the warehouse to be used upon invoicing.
    """,
    "category": "Sales/Sales",
    "depends": ["sale_stock", "account"],
    "external_dependencies": {},
    "data": [
        # Views
        "views/stock_warehouse_views.xml",
    ],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
