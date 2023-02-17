# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    template_type = fields.Selection(string='Template Type',
                                     selection=[('teleprince', 'TelePrince'), ('teleprince_b_and_o', 'Teleprince & B&O')], default='teleprince_b_and_o')
