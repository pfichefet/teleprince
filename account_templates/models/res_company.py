from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    teleprince_logo = fields.Binary(string="Teleprince Logo")
    b_and_o_logo = fields.Binary(string="B&O Logo")
