from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_partner_id  = fields.Many2one('res.partner', string="Customer", compute='_compute_sales_partner_id', search="_search_sale_partner_id", help="Customer of the main sale order")

    def _compute_sales_partner_id(self):
        """
        Get the partner of the first sale order
        """
        for po in self:
            sale_orders = po._get_sale_orders()
            if sale_orders:
                po.sale_partner_id = sale_orders[0].partner_id
            else:
                po.sale_partner_id = False

    def _search_sale_partner_id(self, operator, value):
        """
        Search method to enable searching on the computed field sale_partner_id
        """
        if not value:
            # Handle the 'is set' and 'is not set' filters
            sale_domain = []
            final_operator = 'not in' if operator == '=' else 'in'
        else:
            # Handle other filters
            sale_domain = [('partner_id', operator, value)]
            final_operator = '='
        sale_orders = self.env['sale.order'].search(sale_domain)
        purchase_order_ids = sale_orders._get_purchase_orders().ids
        return [('id', final_operator, purchase_order_ids)]
