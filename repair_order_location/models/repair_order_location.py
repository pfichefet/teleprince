from odoo import fields, models


class RepairOrderLocation(models.Model):
    _name = "repair.order.location"
    _description = "Repair Order Location"

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Name", required=True)
