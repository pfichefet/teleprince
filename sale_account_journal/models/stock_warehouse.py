from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    sale_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Sales Journal",
        domain=[("type", "=", "sale")],
        check_company=True,
        help="During the invoicing process, this journal "
        "is used for sales orders associated with this warehouse.",
    )
