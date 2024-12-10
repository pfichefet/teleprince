from odoo import api, fields, models, _


class BOReportLineSale(models.Model):
    _name = 'bo.report.line.sale'
    _inherit = 'bo.report.line.abstract'
    _description = "B&O report line sale"

    pos_order_line_id = fields.Many2one('pos.order.line', string='Pos Order Line', readonly=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', readonly=True)
    order_id = fields.Many2one('sale.order', string='Sale Order', related='sale_line_id.order_id')
    pos_order_id = fields.Many2one('pos.order', string='¨POS Order', related='pos_order_line_id.order_id')

    @api.depends('product_id', 'lot_id', 'order_id')
    def _compute_name(self):
        """
        Compute the name of the line
        """
        line_with_name_set = self.env['bo.report.line.sale']
        for line in self:
            name = False
            order = line.order_id or line.pos_order_id or False
            if order:
                name = f"{order.display_name} - {line.product_id.display_name}"
                if line.lot_id:
                    name += f"- {line.lot_id.name}"
            elif line.name:
                name = line.name
            if name:
                line.name = name
                line_with_name_set |= line
        super(BOReportLineSale, self - line_with_name_set)._compute_name()

    def prepare_api_json_values(self):
        """
        Override method
        Add parameters for the sale report.
        """
        values = super().prepare_api_json_values()
        date = self.date
        order = self.order_id or self.pos_order_id
        values.update({
            "salesDate": date.strftime('%Y-%m-%d'),
            "salesNo": order.name if order else "",
            "SoldQuantity": str(self.quantity),
        })
        return values
