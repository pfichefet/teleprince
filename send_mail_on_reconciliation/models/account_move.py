# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
	_inherit = 'account.move'

	@api.depends('amount_residual', 'move_type', 'state', 'company_id')
	def _compute_payment_state(self):
		res = super(AccountMove, self)._compute_payment_state()
		for rec in self:
			if rec.payment_state == 'paid':
				template = self.env.ref('send_mail_on_reconciliation.email_template_invoice_paid', raise_if_not_found=False)
				template.sudo().send_mail(rec.id, force_send=True)
		return res
