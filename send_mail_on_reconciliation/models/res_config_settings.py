from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    send_mail_invoice_reconciliation = fields.Boolean(string="Send mail to the customer when his invoice is reconciled", related="company_id.send_mail_invoice_reconciliation", readonly=False)
    invoice_reconciliation_mail_template_id = fields.Many2one("mail.template", string="Mail template used for invoice reconciliation", related="company_id.invoice_reconciliation_mail_template_id", readonly=False)
