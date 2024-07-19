# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
import requests
import urllib.request, json
from odoo.addons.sale_inventory_api.API.post_sale_inventory import PostSaleInventory
from datetime import datetime
_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit = "stock.quant"

    api_triggered = fields.Boolean(string="BO Api Triggered", default=False)
    is_display_product = fields.Boolean(string="Dispaly Product", copy=False)

    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id','is_display_product','api_triggered'] + self._get_inventory_fields_write()
    
    def post_quant_data(self):
        """
        Post Quant Data
        :return: True
        """
        quant_list = []
        company_ids = self.env['res.company'].search([('b_and_o_store_id', '!=', 0)])
        for company_rec in company_ids:
            print ("company_reccompany_reccompany_rec", company_rec.b_and_o_store_id)
            quants = self.search([('inventory_quantity_set', '=', False),
                                     ('company_id', '=', company_rec.id)])
            quant_ids = quants.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
            print ("quant_idsquant_ids=>>>>>>>>>>>>>>>", quant_ids)
            _logger.info("quant_ids %s", quant_ids)
            for quant in quant_ids:
                today_date = datetime.today()
                year, month, day, hour, minute, second = today_date.timetuple()[:6]
                inventoryStatus = 'Sellable'
                if quant.is_display_product or quant.product_id.sale_ok is False:
                    inventoryStatus = 'Display'
                elif quant.reserved_quantity:
                    inventoryStatus = 'Reserved'
                elif quant.available_quantity:
                    inventoryStatus = 'Sellable'
                elif quant.location_id and quant.location_id.scrap_location:
                    inventoryStatus = 'Non-Sellable'
                
                print ("inventoryStatusinventoryStatus", inventoryStatus)
                _logger.info("name %s", quant.product_id.name)
                _logger.info("default code %s", quant.product_id.default_code)
                if quant.lot_id:
                    quant_list.append({
                        "storeId": company_rec.b_and_o_store_id,
                        "productNo": quant.product_id and quant.product_id.default_code and int(quant.product_id.default_code) or quant.product_id.id,
                        "onhandQuantity": quant.quantity > 0 and quant.quantity or 0,
                        "inventoryDate": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.0000Z",
                        "productDescription": quant.product_id.name[:100],
                        "storeName": company_rec.name,
                        "inventoryStatus": inventoryStatus,
                        "serialNumber": quant.lot_id.name.strip(),
                        "lineNo": quant.id,
                    })
                else:
                    quant_list.append({
                        "storeId": company_rec.b_and_o_store_id,
                        "productNo": quant.product_id and quant.product_id.default_code and int(quant.product_id.default_code) or quant.product_id.id,
                        "onhandQuantity": quant.quantity > 0 and quant.quantity or 0,
                        "inventoryDate": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.0000Z",
                        "productDescription": quant.product_id.name[:100],
                        "storeName": company_rec.name,
                        "inventoryStatus": inventoryStatus,
                        "lineNo": quant.id,
                    })
                if not quant.api_triggered:
                    quant.api_triggered = True
            if quant_list:
                post_sale_inventory_api = PostSaleInventory(
                    company_rec.b_and_o_api_key, company_rec.b_and_o_api_environment
                )
                post_sale_inventory_api.post_inventory_data(quant_list)
        return True
