from odoo import models, fields, api, _


class StockQuant(models.Model):
    _inherit = "stock.quant"

    is_display_product = fields.Boolean(string="Dispaly Product", copy=False)

    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        fields_to_create = super()._get_inventory_fields_create()
        return fields_to_create + ['is_display_product']

    def prepare_bo_report_line(self, report):
        self.ensure_one()
        values = {
            "quant_id": self.id,
            "report_id": report.id,
            "warehouse_id": self.location_id.warehouse_id.id,
            "date": fields.Date.today(),
            "product_id": self.product_id.id,
            "quantity": self.quantity,
            "uom_id": self.product_uom_id.id,
            "lot_id": self.lot_id.id,
            "company_id": self.company_id.id,
        }
        return values
