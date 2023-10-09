# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	line_taxed_total = fields.Float(string="Taxed Total", compute='_compute_tax_totals')

	@api.depends('product_uom_qty', 'price_unit', 'tax_id')
	def _compute_tax_totals(self):
		for order in self:
			order.line_taxed_total = order.product_uom_qty * order.price_unit
