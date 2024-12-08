from odoo import fields, models, _


class BOReportLineSale(models.Model):
    _name = 'bo.report.line.sale'
    _inherit = 'bo.report.line.abstract'
    _description = "B&O report line sale"

    sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', readonly=True)
    order_id = fields.Many2one('sale.order', string='Sale Order', related='sale_line_id.order_id')

    def prepare_api_json_values(self):
        """
        Override method
        Add parameters for the sale report.
        """
        list_values = super().prepare_api_json_values()
        for values in list_values:
            date = self.date
            values.update({
                "salesDate": date.strftime('%Y-%m-%d'),
                "salesNo": self.order_id.name if self.order_id else "",
                "SoldQuantity": str(self.quantity),
            })
        return list_values
