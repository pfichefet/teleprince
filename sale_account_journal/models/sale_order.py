from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.warehouse_id.sale_journal_id:
            invoice_vals['journal_id'] = self.warehouse_id.sale_journal_id.id
        return invoice_vals
