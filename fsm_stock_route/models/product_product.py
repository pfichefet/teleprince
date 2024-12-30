from collections import defaultdict
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _inverse_fsm_quantity(self):
        """
        Overwrite method
        Part that is modified start and end with a comment.
        Custom code Start
        *** Modified part ***
        Custom code End

        Sale order line created use the route specified in the project settings of the task.
        """
        task = self._get_contextual_fsm_task()
        if task:
            SaleOrderLine_sudo = self.env['sale.order.line'].sudo()
            sale_lines_read_group = SaleOrderLine_sudo._read_group([
                ('order_id', '=', task.sale_order_id.id),
                ('product_id', 'in', self.ids),
                ('task_id', '=', task.id)],
                ['product_id', 'sequence', 'ids:array_agg(id)'],
                ['product_id', 'sequence'],
                lazy=False)
            sale_lines_per_product = defaultdict(lambda: self.env['sale.order.line'])
            for sol in sale_lines_read_group:
                sale_lines_per_product[sol['product_id'][0]] |= SaleOrderLine_sudo.browse(sol['ids'])
            for product in self:
                sale_lines = sale_lines_per_product.get(product.id, self.env['sale.order.line'])
                all_editable_lines = sale_lines.filtered(lambda l: l.qty_delivered == 0 or l.qty_delivered_method == 'manual' or l.state != 'done')
                diff_qty = product.fsm_quantity - sum(sale_lines.mapped('product_uom_qty'))
                if all_editable_lines:  # existing line: change ordered qty (and delivered, if delivered method)
                    if diff_qty > 0:
                        vals = {
                            'product_uom_qty': all_editable_lines[0].product_uom_qty + diff_qty,
                        }
                        if all_editable_lines[0].qty_delivered_method == 'manual':
                            vals['qty_delivered'] = all_editable_lines[0].product_uom_qty + diff_qty
                        all_editable_lines[0].with_context(fsm_no_message_post=True).write(vals)
                        continue
                    # diff_qty is negative, we remove the quantities from existing editable lines:
                    for line in all_editable_lines:
                        new_line_qty = max(0, line.product_uom_qty + diff_qty)
                        diff_qty += line.product_uom_qty - new_line_qty
                        vals = {
                            'product_uom_qty': new_line_qty
                        }
                        if line.qty_delivered_method == 'manual':
                            vals['qty_delivered'] = new_line_qty
                        line.with_context(fsm_no_message_post=True).write(vals)
                        if diff_qty == 0:
                            break
                elif diff_qty > 0:  # create new SOL
                    # Custom code Start
                    warehouse = task.sale_order_id.warehouse_id
                    # Custom code End
                    vals = {
                        'order_id': task.sale_order_id.id,
                        'product_id': product.id,
                        'product_uom_qty': diff_qty,
                        'product_uom': product.uom_id.id,
                        'task_id': task.id,
                        # Custom code Start
                        'route_id': warehouse.fsm_route_id.id if warehouse.fsm_route_id else False,
                        # Custom code End
                    }
                    if product.service_type == 'manual':
                        vals['qty_delivered'] = diff_qty

                    sol = SaleOrderLine_sudo.create(vals)
                    if task.sale_order_id.pricelist_id.discount_policy != 'without_discount':
                        sol.discount = 0.0
                    if not sol.qty_delivered_method == 'manual':
                        sol.qty_delivered = 0
