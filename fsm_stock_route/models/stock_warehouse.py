from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    fsm_route_id = fields.Many2one("stock.route", string="Route", domain=[('sale_selectable', '=', True)], help="Sales order lines created through the Field Service app for this warehouse will follow this route.")
