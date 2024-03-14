# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import urllib.request, json
from odoo.addons.sale_inventory_api.API.post_sale_inventory import PostSaleInventory
from datetime import datetime


class StockQuant(models.Model):
    _inherit = "stock.quant"

    api_triggered = fields.Boolean(string="BO Api Triggered", default=False)

    def post_quant_data(self):
        """
        Post Quant Data
        :return: True
        """
        quant_list = []
        company_ids = self.env['res.company'].search([('b_and_o_store_id', '!=', False)])
        for company_rec in company_ids:
            quant_ids = self.search([('inventory_quantity_set', '=', False),
                                     ('company_id', '=', company_rec.id)])
            for quant in quant_ids:
                today_date = datetime.today()
                year, month, day, hour, minute, second = today_date.timetuple()[:6]
                inventoryStatus = 'Sellable'
                if quant.product_id.sale_ok is False:
                    inventoryStatus = 'Display'
                elif quant.reserved_quantity:
                    inventoryStatus = 'Reserved'
                elif quant.available_quantity:
                    inventoryStatus = 'Sellable'
                elif quant.location_id and quant.location_id.scrap_location:
                    inventoryStatus = 'Non-Sellable'
                
                if quant.lot_id:
                    quant_list.append({
                        "storeId": company_rec.b_and_o_store_id,
                        "productNo": quant.product_id.id,
                        "onhandQuantity": quant.quantity,
                        "inventoryDate": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.0000Z",
                        "productDescription": quant.product_id.name[:100],
                        "storeName": company_rec.name,
                        "inventoryStatus": inventoryStatus,
                        "serialNumber": quant.lot_id.name.strip()
                    })
                else:
                    quant_list.append({
                        "storeId": company_rec.b_and_o_store_id,
                        "productNo": quant.product_id.id,
                        "onhandQuantity": quant.quantity,
                        "inventoryDate": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.0000Z",
                        "productDescription": quant.product_id.name[:100],
                        "storeName": company_rec.name,
                        "inventoryStatus": inventoryStatus,
                    })
                if not quant.api_triggered:
                    quant.api_triggered = False
            if quant_list:
                post_sale_inventory_api = PostSaleInventory(
                    company_rec.b_and_o_api_key, company_rec.b_and_o_api_environment
                )
                post_sale_inventory_api.post_inventory_data(quant_list)
        return True
