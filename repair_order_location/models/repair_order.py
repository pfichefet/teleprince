from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    ro_location_id = fields.Many2one("repair.order.location", string="Location", ondelete="set null")
