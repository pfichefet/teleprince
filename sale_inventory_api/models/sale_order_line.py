from odoo import api, fields, models
from odoo.tools import float_is_zero


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    invoice_date = fields.Date(string='Invoice Date', compute='_compute_invoice_date', store=True)

    @api.depends('invoice_lines', 'invoice_lines.date', 'pos_order_line_ids', 'pos_order_line_ids.order_id.date_order')
    def _compute_invoice_date(self):
        """
        Compute the invoice date of a line.
        In case of multiple invoices the date is the earliest.
        """
        for line in self:
            list_invoice_date = line.invoice_lines.filtered(lambda inv_line: inv_line.move_id.state == 'posted').mapped('date')
            list_pos_order_date = line.pos_order_line_ids.order_id.filtered(lambda pos_order: pos_order.state in ['paid', 'done', 'invoiced']).mapped('date_order')
            if list_invoice_date:
                line.invoice_date = min(list_invoice_date)
            elif list_pos_order_date:
                line.invoice_date = min(list_pos_order_date)
            else:
                line.invoice_date = False

    def prepare_bo_report_line(self, report):
        """
        Create on B&O report line per serial number.
        If not serial number are linked to this sale order we send the ordered quantity without SN details.
        """
        self.ensure_one()
        sn_values = []
        base_values = {
            "sale_line_id": self.id,
            "report_id": report.id,
            "warehouse_id": self.warehouse_id.id,
            "date": self.invoice_date,
            "product_id": self.product_id.id,
            "company_id": self.company_id.id,
        }
        move_quantity = 0.0
        for stock_move in self.move_ids:
            for sml in stock_move.move_line_ids:
                values = base_values.copy()
                values.update({
                    "quantity": sml.qty_done,
                    "lot_id": sml.lot_id.id,
                    "uom_id": sml.product_uom_id.id,
                })
                move_quantity += sml.product_uom_id._compute_quantity(sml.qty_done, self.product_uom)
                sn_values.append(values)
        quantity_left = self.product_uom_qty - move_quantity
        if not float_is_zero(quantity_left, precision_rounding=self.product_uom.rounding):
            values = base_values.copy()
            values.update({
                "quantity": quantity_left,
                "uom_id": self.product_uom.id,
            })
            sn_values.append(values)
        return sn_values
