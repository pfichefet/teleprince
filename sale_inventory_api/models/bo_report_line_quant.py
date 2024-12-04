from odoo import fields, models, _


class BOReportLineQuant(models.Model):
    _name = 'bo.report.line.quant'
    _inherit = 'bo.report.line.abstract'
    _description = "B&O report line quant"

    quant_id = fields.Many2one('stock.quant', string='Stock Quant', required=True, readonly=True)
    quant_lot_id = fields.Many2one('stock.lot', string='Lot Quant', related='quant_id.lot_id')
    lot_id = fields.Many2one(domain="[('id', '=', quant_lot_id)]")  # Field define in abstract model add a domain

    def prepare_api_json_values(self):
        """
        Override method
        Add parameters for the inventory report.
        """
        list_values = super().prepare_api_json_values()
        for values in list_values:
            date = self.date
            quant = self.quant_id
            inventory_status = 'Sellable'
            if quant.is_display_product or not quant.product_id.sale_ok:
                inventory_status = 'Display'
            elif quant.reserved_quantity:
                inventory_status = 'Reserved'
            values.update({
                "inventoryDate": date.strftime('%Y-%m-%d'),
                "inventorystatus": inventory_status,
                "inventoryQuantity": str(quant.available_quantity),
                "unitofmeasure": self.uom_id.name,
            })
            if inventory_status == 'Reserved':
                reserved_values = values.copy()
                reserved_values.update({
                    "inventoryQuantity": str(quant.reserved_quantity),
                })
        return list_values
