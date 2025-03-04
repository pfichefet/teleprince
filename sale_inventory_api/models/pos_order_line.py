from odoo import models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    def prepare_bo_report_line(self, report):
        """
        Create on B&O report line per serial number.
        If not serial number are linked to this sale order we send the ordered quantity without SN details.
        """
        self.ensure_one()
        sn_values = []
        base_values = {
            "pos_order_line_id": self.id,
            "report_id": report.id,
            "warehouse_id": self.order_id.picking_type_id.warehouse_id.id if self.order_id.picking_type_id else False,
            "date": self.order_id.date_order,
            "product_id": self.product_id.id,
            "company_id": self.company_id.id,
            "quantity": self.qty,
            "uom_id": self.product_uom_id.id,
        }
        if self.pack_lot_ids:
            qty = self.qty / len(self.pack_lot_ids)
            for pack_lot in self.pack_lot_ids:
                lot_name = pack_lot.lot_name
                product = pack_lot.product_id
                existing_lot = self.env['stock.lot'].search(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id),
                                                             ('product_id', '=', product.id), ('name', '=', lot_name)], limit=1)
                if existing_lot:
                    values = base_values.copy()
                    values.update({
                        "lot_id": existing_lot.id,
                        "quantity": qty,
                    })
                    sn_values.append(values)
        if not sn_values:
            sn_values = [base_values]
        return sn_values
