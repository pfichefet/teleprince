from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    store_identifier = fields.Integer(string="Store Identifier")
