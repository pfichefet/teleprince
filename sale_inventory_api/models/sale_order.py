# -*- coding: utf-8 -*-

import requests
from odoo import models, fields, api, _


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	api_triggered = fields.Boolean(string="Api Triggered")

	# def send_api_data(self):
	#     print("cron send api data")
	#
	#

	def prepare_sale_data(self):
		sale_data = {}

		# sale_data_list = []
		# for rec in self:
		#     sale_data_list.append()
		#
		#
		# [
		#
		# 	{
		#
		# 		"storeId": 20929,
		#
		# 		"productNo": 1646300,
		#
		# 		"lineQuantity": 0,
		#
		# 		"salesDate": "2021-03-17T07:16:17.352Z",
		#
		# 		"salesReference": "string",
		#
		# 		"lineNo": 0,
		#
		# 		"productDescription": "string",
		#
		# 		"serialNumber": "string",
		#
		# 		"storeName": "string"
		#
		# 	}

		# ]
		for product in self:
			sale_data = {'storeId': 20929,
			             'productNo': product.barcode,
			             'lineQuantity': sale_order_line.product_uom_qty,
			             'salesDate': str(self.date_order),
			             'salesReference': self.name,
			             'lineNo': self.order_line.id,
			             'productDescription': product.name,
			             'serialNumber': 'not required',
			             'storeName': self.company.name,
			             }

		data_dict = [{'storeId': 20929,
		              'productNo': 120,
		              'lineQuantity': 120,
		              'salesDate': "2021-03-17T07:16:17.352Z",
		              'salesReference': 'Sale Ref',
		              'lineNo': 4545,
		              'productDescription': 'Product Disc',
		              'serialNumber': "1234",
		              'storeName': 'My Store',
		              }]
		print("----DATA----", data_dict)
		return data_dict

	@api.model
	def post_sale_data(self):
		url = "https://test.api.bang-olufsen.dk/posdata/v1-test/api/Sale"
		headers = {
			"Content-Type": "application/json",
			"Ocp-Apim-Subscription-Key": "d83f37a2e6da4fe5a078b2388d8c5972",
		}

		# try:
		response = requests.post(
			url,
			json=self.env['sale.order'].search([], limit=1).prepare_sale_data(),
			headers=headers,
			# auth=('78e9573f855349fcbe51ea6fac62c7e4')
		)
		# import pdb;pdb.set_trace()
		# print(">>>>>>>>>>. response", response.json())
		response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
		return response.json()
	# except requests.exceptions.RequestException as e:
	# 	print(f"Error occurred: {e}")
	# 	return None
