# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    email_accountant_template_id = fields.Many2one("mail.template", string="Email Accountant Template")
    refund_email_accountant_template_id = fields.Many2one("mail.template", string="Refund Email Accountant Template")
