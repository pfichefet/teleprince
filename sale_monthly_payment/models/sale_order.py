from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    with_financing = fields.Boolean(string="With Financing")
    monthly_financing_payment = fields.Monetary(string="Monthly Financing Payment")
