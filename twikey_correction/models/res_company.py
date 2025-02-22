from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    twikey_base_url = fields.Char(groups="base.group_user")
    twikey_api_key = fields.Char(groups="base.group_user")

    twikey_auto_collect = fields.Boolean(groups="base.group_user")
    twikey_send_pdf = fields.Boolean(groups="base.group_user")
    twikey_send_invoice = fields.Boolean(groups="base.group_user")
    twikey_include_purchase = fields.Boolean(groups="base.group_user")

    mandate_feed_pos = fields.Integer(groups="base.group_user", readonly=True)
    invoice_feed_pos = fields.Integer(groups="base.group_user", readonly=True)
