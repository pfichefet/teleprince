{
    "name": "Sale Purchase Addons",
    "version": "2.0.1",
    "summary": "Addons to the workflow between sale and purchase order.",
    "sequence": 10,
    "author": "The Fish Consulting",
    "website": "https://thefishconsulting.be",
    "description": """
Sale Purchase Addons
====================
Add the customer of the sale order link to the purchase order on the purchase order.
    """,
    "category": "Hidden",
    "depends": ["sale_purchase"],
    "external_dependencies": {},
    "data": [
        # Views
        "views/purchase_order_views.xml",
    ],
    "price": 0.0,
    "currency": "EUR",
    "support": "contact@thefishconsulting.be",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
