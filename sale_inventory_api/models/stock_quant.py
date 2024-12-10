from odoo import models
from odoo.tools import float_is_zero


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def prepare_bo_report_line(self, report):
        """
        Prepare a dictionary of values to create B&O report line.
        """
        list_values = []
        self.ensure_one()
        values = {
            "quant_id": self.id,
            "report_id": report.id,
            "warehouse_id": self.location_id.warehouse_id.id,
            "date": report.date_start,
            "product_id": self.product_id.id,
            "uom_id": self.product_uom_id.id,
            "lot_id": self.lot_id.id,
            "company_id": self.company_id.id,
        }
        inventory_status = 'Sellable'
        if self:
            if self.location_id.is_display_location:
                inventory_status = 'Display'
            elif float_is_zero(self.reserved_quantity, precision_rounding=self.product_uom_id.rounding):
                inventory_status = 'Reserved'
        if inventory_status == 'Reserved':
            values.update({
                "inventory_status": inventory_status,
                "quantity": str(self.reserved_quantity),
            })
            if not float_is_zero(self.available_quantity, precision_rounding=self.product_uom_id.rounding):
                values2 = values.copy()
                values2.update({
                    "inventory_status": 'Sellable',
                    "quantity": str(self.available_quantity),
                })
                list_values.append(values2)
        else:
            values.update({
                "inventory_status": inventory_status,
                "quantity": str(self.available_quantity),
            })
        list_values.append(values)
        return list_values
