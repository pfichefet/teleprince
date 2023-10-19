# -*- coding: utf-8 -*-

from odoo import models, fields, _


class Company(models.Model):
    _inherit = "res.company"

    b_and_o_api_environment = fields.Selection(
        [('test', 'Test'), ('prod', 'Production')], default="test"
    )
    b_and_o_api_key = fields.Char(string="API Key")
    b_and_o_store_id = fields.Integer(string="Store ID")
