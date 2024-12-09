# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    send_to_accountant = fields.Boolean(string="Send to Accountant")

    def get_accountant_mail_template(self):
        """
        Return the email template to use depending on the type of the journal entry.
        """
        self.ensure_one()
        if self.move_type in ['in_invoice', 'out_invoice']:
            template = self.journal_id.email_accountant_template_id
        else:
            template = self.journal_id.refund_email_accountant_template_id
        return template

    def send_invoice_to_accountant(self):
        """
        Action called to send Email to accountant.
        """
        journal_without_email_accountant_template = self.env["account.journal"]
        invoices_already_sent = self.env["account.move"]
        invoices_to_sent = self.env["account.move"]
        # We handle error before sending email, since sending email doesn't with for commit.
        for invoice in self.filtered(lambda inv: inv.move_type in ['in_invoice', 'out_invoice', 'in_refund', 'out_refund']):
            template = invoice.get_accountant_mail_template()
            if not template:
                journal_without_email_accountant_template |= invoice.journal_id
            elif invoice.send_to_accountant:
                invoices_already_sent |= invoice
            else:
                invoices_to_sent |= invoice
        if journal_without_email_accountant_template:
            raise UserError(_("Please first define an '(Refund) Email Accountant Template' on journals: %s") % journal_without_email_accountant_template.mapped('name'))
        if invoices_already_sent:
            raise UserError(_("Those invoices / Refunds have already been sent to the accountant: %s") % invoices_already_sent.mapped('name'))
        # Send emails
        for invoice in invoices_to_sent:
            template = invoice.get_accountant_mail_template()
            template.send_mail(invoice.id, force_send=True)
        invoices_to_sent.write({"send_to_accountant": True})
