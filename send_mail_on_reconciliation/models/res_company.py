from odoo import fields, models, _


class Company(models.Model):
    _inherit = "res.company"

    send_mail_invoice_reconciliation = fields.Boolean(string="Send mail to the customer when his invoice is reconciled")
    invoice_reconciliation_mail_template_id = fields.Many2one("mail.template", string="Mail template used for invoice reconciliation", default=lambda self: self.env.ref('send_mail_on_reconciliation.email_template_invoice_paid', raise_if_not_found=False))
