from odoo import fields, models, _


class BOReportLineQuant(models.Model):
    _name = 'bo.report.line.quant'
    _inherit = 'bo.report.line.abstract'
    _description = "B&O report line quant"

    quant_id = fields.Many2one('stock.quant', string='Stock Quant', readonly=True)
    quant_lot_id = fields.Many2one('stock.lot', string='Lot Quant', related='quant_id.lot_id')
    lot_id = fields.Many2one(domain="[('id', '=', quant_lot_id), ('product_id', '=', product_id)]") # Field define in abstract model add a domain
    inventory_status = fields.Char(string='Inventory Status', required=True)

    def prepare_api_json_values(self):
        """
        Override method
        Add parameters for the inventory report.
        """
        values = super().prepare_api_json_values()
        date = self.date
        values.update({
            "inventoryDate": date.strftime('%Y-%m-%d'),
            "inventorystatus": self.inventory_status,
            "inventoryQuantity": str(self.quantity),
            "unitofmeasure": self.uom_id.name if self.uom_id else "",
        })
        return values
