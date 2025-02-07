# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.misc import unquote


class Task(models.Model):
    _inherit = "project.task"

    def _domain_sale_line_id(self):
        """
        Overwrite methode
        Allow to choose a sale order line linked to the partner of the project.
        """
        domain = expression.AND([
            self.env['sale.order.line']._sellable_lines_domain(),
            [
                ('company_id', '=', unquote('company_id')),
                '|', '|',
                    '|',
                        ('order_partner_id', 'child_of', unquote('partner_id if partner_id else []')),
                        ('order_id.partner_shipping_id', 'child_of', unquote('partner_id if partner_id else []')),
                    '|',
                        ('order_partner_id', '=?', unquote('partner_id')),
                        ('order_id.partner_shipping_id', '=?', unquote('partner_id')),
                    '|',
                        ('order_partner_id', '=?', unquote('project_partner_id')),
                        ('order_id.partner_shipping_id', '=?', unquote('project_partner_id')),
                ('is_service', '=', True), ('is_expense', '=', False), ('state', 'in', ['sale', 'done']),
            ],
        ])
        return domain

    project_partner_id = fields.Many2one("res.partner", string="Project Partner", related="project_id.partner_id")
