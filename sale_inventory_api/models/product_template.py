from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_api_b_and_o_compliant = fields.Boolean(string="Send To B&O API",
                                              compute="_compute_is_api_b_and_o_compliant",
                                              readonly=False, store=True, precompute=True)

    @api.depends('seller_ids', 'seller_ids.partner_id.is_b_and_o_supplier')
    def _compute_is_api_b_and_o_compliant(self):
        """
        A product is compliant with the B&O API by default if its supplier is B&O.
        """
        for product in self:
            if not product.is_api_b_and_o_compliant:
                for seller in product.seller_ids:
                    if seller.partner_id.is_b_and_o_supplier:
                        product.is_api_b_and_o_compliant = True
                        break
