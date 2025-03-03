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
        self = self.with_context(industry_fsm_stock_set_quantity=True)
        task = self._get_contextual_fsm_task()
        if task:
            SaleOrderLine_sudo = self.env['sale.order.line'].sudo()
            sale_lines_read_group = SaleOrderLine_sudo._read_group([
                ('order_id', '=', task.sale_order_id.id),
                ('product_id', 'in', self.ids),
                ('task_id', '=', task.id)],
                ['product_id', 'sequence'],
                ['id:array_agg'])
            sale_lines_per_product = defaultdict(lambda: self.env['sale.order.line'])
            for product, __, ids in sale_lines_read_group:
                sale_lines_per_product[product.id] |= SaleOrderLine_sudo.browse(ids)
            for product in self:
                sale_lines = sale_lines_per_product.get(product.id, self.env['sale.order.line'])
                all_editable_lines = sale_lines.filtered(lambda l: l.qty_delivered == 0 or l.qty_delivered_method == 'manual' or not l.order_id.locked)
                diff_qty = product.fsm_quantity - sum(sale_lines.mapped('product_uom_qty'))
                if all_editable_lines:  # existing line: change ordered qty (and delivered, if delivered method)
                    if diff_qty > 0:
                        vals = {
                            'product_uom_qty': all_editable_lines[0].product_uom_qty + diff_qty,
                        }
                        if task.under_warranty:
                            vals['price_unit'] = 0
                        if product.service_type == 'manual':
                            vals['qty_delivered'] = all_editable_lines[0].product_uom_qty + diff_qty
                        all_editable_lines[0].with_context(fsm_no_message_post=True).write(vals)
                        continue
                    # diff_qty is negative, we remove the quantities from existing editable lines:
                    for line in all_editable_lines:
                        new_line_qty = max(0, line.product_uom_qty + diff_qty)
                        diff_qty += line.product_uom_qty - new_line_qty
                        if product.service_type == 'manual':
                            line.with_context(fsm_no_message_post=True).qty_delivered = new_line_qty
                        line.with_context(fsm_no_message_post=True).product_uom_qty = new_line_qty
                        if task.under_warranty:
                            line.price_unit = 0
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
                    if task.under_warranty:
                        vals['price_unit'] = 0
                    if product.service_type == 'manual':
                        vals['qty_delivered'] = diff_qty
                    if task.sale_order_id.order_line:
                        vals['sequence'] = max(task.sale_order_id.order_line.mapped('sequence')) + 1

                    sol_sudo = SaleOrderLine_sudo.create(vals)