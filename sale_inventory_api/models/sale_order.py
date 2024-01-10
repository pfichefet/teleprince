# -*- coding: utf-8 -*-

import requests
from odoo import models, fields, api, _
from odoo.addons.sale_inventory_api.API.post_sale_inventory import PostSaleInventory


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	api_triggered = fields.Boolean(string="BO Api Triggered", default=False)

	@api.model
	def post_sale_order_data(self):
		"""
		Post Sale order data which has the invoices and once the sale confirmed
		:return:
		"""
		sale_line_list = []
		sale_order_ids = self.search([('state', '=', 'sale'), ('invoice_ids', 'not in', []), ('api_triggered', '=', False), ('date_order', '!=', False)])
		for sale_line in sale_order_ids.mapped('order_line').filtered('product_id'):
			order_id = sale_line.order_id
			year, month, day, hour, minute, second = order_id.date_order.timetuple()[:6]
			sale_line_list.append({
				"storeId": self.env.company.b_and_o_store_id,
				"productNo": sale_line.product_id.id,
				"lineQuantity": sale_line.product_uom_qty,
				"salesDate": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.0000Z",
				"salesReference": order_id.name,
				"lineNo": sale_line.id,
				"productDescription": sale_line.product_id.name[:100],
				"storeName": order_id.company_id.name,
			})
			if not order_id.api_triggered:
				order_id.api_triggered = True
		if sale_line_list:
			post_sale_inventory_api = PostSaleInventory(self.env.company.b_and_o_api_key, self.env.company.b_and_o_api_environment)
			return post_sale_inventory_api.post_sale_data(sale_line_list)
		else:
			return True
