from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_b_and_o_supplier = fields.Boolean(string="Is B&O Supplier")
