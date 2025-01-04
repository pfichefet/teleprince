# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
	_inherit = 'account.move'

	send_mail_invoice_reconciliation = fields.Boolean(string="Send mail to the customer when his invoice is reconciled", compute="_compute_send_mail_invoice_reconciliation", precompute=True, store=True, readonly=False)

	@api.depends('amount_residual', 'move_type', 'state', 'company_id')
	def _compute_payment_state(self):
		"""
		Send an Email to inform a customer that his invoice has been reconciled.
		"""
		res = super(AccountMove, self)._compute_payment_state()
		for invoice in self:
			if invoice.payment_state == 'paid' and invoice.send_mail_invoice_reconciliation:
				template = invoice.company_id.invoice_reconciliation_mail_template_id
				if template:
					template.sudo().send_mail(invoice.id, force_send=True)
		return res

	@api.depends('company_id', 'move_type', 'pos_order_ids')
	def _compute_send_mail_invoice_reconciliation(self):
		"""
		Compute whether an Email should be sent to inform a customer that his invoice has been reconciled.
		"""
		for invoice in self:
			# Invoices that has been paid through a point of sale should not inform the customer that the invoice has been reconciled.
			if invoice.pos_order_ids:
				invoice.send_mail_invoice_reconciliation = False
			elif invoice.move_type == 'out_invoice' and invoice.company_id.send_mail_invoice_reconciliation:
				invoice.send_mail_invoice_reconciliation = True
			else:
				invoice.send_mail_invoice_reconciliation = False
