from odoo import models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    def prepare_bo_report_line(self, report):
        """
        Create on B&O report line per serial number.
        If not serial number are linked to this sale order we send the ordered quantity without SN details.
        """
        self.ensure_one()
        values = {
            "pos_order_line_id": self.id,
            "report_id": report.id,
            "warehouse_id": self.order_id.picking_type_id.warehouse_id.id if self.order_id.picking_type_id else False,
            "date": self.order_id.date_order,
            "product_id": self.product_id.id,
            "company_id": self.company_id.id,
            "quantity": self.qty,
        }
        # if self.pack_lot_ids:
        #     values.update({
        #         "lot_id": self.pack_lot_ids[0].id,
        #     })
        return values
