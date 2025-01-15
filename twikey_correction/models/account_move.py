from odoo import api, fields, models



class AccountInvoice(models.Model):
    _inherit = "account.move"

    is_twikey_eligable = fields.Boolean(
        compute_sudo=True,
    ) # add compute sudo

    @api.depends("move_type")
    def _compute_twikey_eligable(self):
        """
        Only certain types of account moves can be sent to Twikey.
        """
        for move in self:
            if move.company_id.twikey_include_purchase:
                move.is_twikey_eligable = move.move_type in ["in_invoice", "out_invoice", "out_refund"]
            else:
                move.is_twikey_eligable = move.move_type in ["out_invoice", "out_refund"]

    @api.depends('twikey_invoice_identifier')
    def _compute_link_html(self):
        for record in self:
            # Generate the HTML link
            record.id_and_link_html = f'<a href="{record.twikey_url}" target="twikey">{record.twikey_invoice_identifier}</a>'
