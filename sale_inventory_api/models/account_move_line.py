# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import urllib.request, json


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def prepare_and_send_invoice_data(self):
        # sale_data = {'storeId': 20929,
        #              'productNo': product.barcode,
        #              'lineQuantity': sale_order_line.product_uom_qty,
        #              'salesDate': str(self.date_order),
        #              'salesReference': self.name,
        #              'lineNo': self.order_line.id,
        #              'productDescription': product.name,
        #              'serialNumber': 'not required',
        #              'storeName': self.company.name,
        #              }
        # sale_data_list = []
        # for rec in self:
        #     sale_data_list.append()

        # temp_dict = { 'storeId': 20929,
        #         'productNo': rec.product_id.id,
        #         'lineQuantity': float(rec.quantity),
        #         'salesDate': str(self.move_id.date),
        #         # 'salesReference': self.name,
        #         'lineNo': self.move_id.id,
        #         'productDescription': rec.product_id.name,
        #         'storeName': self.company_id.name,}

        self.get_response([{'storeId': 20929,
                            'productNo': 1,
                            'lineQuantity': 20,
                            'salesDate': "23-09-2023",
                            # 'salesReference': self.name,
                            'lineNo': 7,
                            'productDescription': 'My Product',
                            'storeName': 'abc', }])
        # for rec in self:
        # response = {'storeId': 20929,
        #             'productNo': 1,
        #             'lineQuantity': 20,
        #             'salesDate': "23-09-2023",
        #             # 'salesReference': self.name,
        #             'lineNo': 7,
        #             'productDescription': 'My Product',
        #             'storeName': 'self.company_id.name', }
        # response = [20929, 1, 20, "23-09-2023", 7, 'My Product', 'self.company_id.name']
        #
        # return response

    def get_response(self, data):
        url = "https://api.bang-olufsen.dk/posdata/v1-test/api/Sale"

        hdr = {
            # Request headers
            'Content-Type': 'application/json-patch+json',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': 'd83f37a2e6da4fe5a078b2388d8c5972',
        }

        # data = {'storeId': 20929,
        #             'productNo': 1,
        #             'lineQuantity': 20,
        #             'salesDate': "23-09-2023",
        #             # 'salesReference': self.name,
        #             'lineNo': 7,
        #             'productDescription': 'My Product',
        #             'storeName': 'self.company_id.name', }
        # data =  [20929, 1, 20, "23-09-2023", 7, 'My Product', 'self.company_id.name']
        # Request body
        data = json.dumps(data)
        response = requests.post(url, headers=hdr, json=data)
        # print(">>>>>>response.json()",
        # import pdb;
        # pdb.set_trace()
        return response

    def post_invoice_data(self):
        # import urllib.request, json
        # try:
        #     url = "https://api.bang-olufsen.dk/posdata/v1-test/api/Sale"
        #
        #     hdr = {
        #         'Content-Type': 'application/json-patch+json',
        #         'Cache-Control': 'no-cache',
        #         'Ocp-Apim-Subscription-Key': 'd83f37a2e6da4fe5a078b2388d8c5972',
        #     }
        #
        #     data = self.env['account.move.line'].search([], limit=1).prepare_and_send_invoice_data()
        #
        #     req = urllib.request.Request(url, headers=hdr, data=json.dumps(data).encode('utf-8'))
        #
        #     req.get_method = lambda: 'POST'
        #     response = urllib.request.urlopen(req)
        #
        #     print(response.getcode())
        #     print(response.read())
        # except Exception as e:
        #     print(e)

        # @api.model
        # def post_invoice_data(self):
        #     url = "https://api.bang-olufsen.dk/posdata/v1-test/api/Sale"
        # headers = {
        #     "Content-Type": "application/json-patch+json",
        #     "Ocp-Apim-Subscription-Key": "d83f37a2e6da4fe5a078b2388d8c5972"
        # }
        #
        # try:
        #     data = self.env['account.move.line'].search([], limit=1).prepare_invoice_data()
        #     data = json.dumps(data)
        #     req = urllib.request.Request(url, headers=headers, data=bytes(data.encode("utf-8")))
        #
        #     req.get_method = lambda: 'POST'
        #     response = urllib.request.urlopen(req)
        #     print("---trieddd---")
        #     print(response.getcode())
        #     print(response.read())
        #
        # except Exception as e:
        #     print(e)
        # try:
        #     response = requests.post(
        #         url,
        #         json=self.env['account.move.line'].search([], limit=1).prepare_invoice_data(),
        #         headers=headers,
        #         auth=("thana@teleprince.be", "Teleprince1")
        #     )
        #     response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        #     return response.json()
        # except requests.exceptions.RequestException as e:
        #     print(f"Error occurred: {e}")
        #     return None

        ########### Python 3.2 #############
        import urllib.request, json
        self.env['account.move.line'].search([], limit=1).prepare_and_send_invoice_data()
        ####################################
