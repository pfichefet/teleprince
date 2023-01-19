# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    teleprince_logo = fields.Binary(related='company_id.teleprince_logo', string="Teleprince Logo", readonly=False)
    b_and_o_logo = fields.Binary(related='company_id.b_and_o_logo', string="B&O Logo", readonly=False)
