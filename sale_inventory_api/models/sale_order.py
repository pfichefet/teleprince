# -*- coding: utf-8 -*-
import logging
import requests
from odoo import models, fields, api, _
from odoo.addons.sale_inventory_api.API.post_sale_inventory import PostSaleInventory
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    default_code = fields.Char(string="Product Reference", required=True)

    @api.constrains('default_code')
    def _check_default_code(self):
    	for record in self:
    		if record.default_code and not record.default_code.isdigit():
    			raise ValidationError(_("Product Reference must be an integer."))

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	api_triggered = fields.Boolean(string="BO Api Triggered", default=False)

	@api.model
	def post_sale_order_data(self):
		"""
		Post Sale order data which has the invoices and once the sale confirmed
		:return:
		"""
		company_ids = self.env['res.company'].search([('b_and_o_store_id', '!=', False)])
		fail_order = []
		for company_rec in company_ids:
			sale_order_ids = self.search([('state', 'in', ['sale', 'done']),
										('invoice_ids', 'not in', []),
										('api_triggered', '=', False),
										('date_order', '!=', False),
										('company_id', '=', company_rec.id)])
			_logger.info("sale_order_ids %s", sale_order_ids)
			sale_line_list = []
			for sale_line in sale_order_ids.mapped('order_line').filtered('product_id'):
				_logger.info("product_id name %s", sale_line.product_id.name)
				_logger.info("product_id code %s", sale_line.product_id.default_code)
				if sale_line.product_id.active == False:
					_logger.info("product_id continuee %s", sale_line.product_id.name)
					continue
				if sale_line.product_id.detailed_type != 'product':
					_logger.info("product_id type continuee %s", sale_line.product_id.name)
					continue
				order_id = sale_line.order_id
				year, month, day, hour, minute, second = order_id.date_order.timetuple()[:6]
				sale_line_list.append({
					"storeId": order_id.company_id.b_and_o_store_id,
					"productNo": sale_line.product_id and int(sale_line.product_id.default_code),
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
				post_sale_inventory_api = PostSaleInventory(company_rec.b_and_o_api_key, company_rec.b_and_o_api_environment)
				post_sale_inventory_api.post_sale_data(sale_line_list)
		return True
