from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_display_location = fields.Boolean(string='Display Location')
