from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.misc import unquote


class Task(models.Model):
    _inherit = "project.task"

    @api.model
    def default_get(self, fields_list):
        """
        Set the default project to the first available FSM project with the display flag set to true
        """
        context = dict(self.env.context)
        is_fsm_mode = self._context.get('fsm_mode')
        fsm_project = False
        if is_fsm_mode and 'project_id' in fields_list and not self._context.get('default_parent_id'):
            company_id = self.env.context.get('default_company_id') or self.env.company.id
            fsm_project = self.env['project.project'].search([('is_fsm', '=', True), ('company_id', '=', company_id), ('display_project_fsm_app', '=', True)], order='sequence, name, id', limit=1)
            if fsm_project:
                context['default_project_id'] = self.env.context.get('default_project_id', fsm_project.id)
        result = super(Task, self.with_context(context)).default_get(fields_list)
        return result

    def _domain_sale_line_id(self):
        """
        Overwrite methode
        Allow to choose a sale order line linked to the partner of the project.
        """
        domain = expression.AND(
            [
                self.env["sale.order.line"]._sellable_lines_domain(),
                [
                    ("company_id", "=", unquote("company_id")),
                    "|",
                    "|",
                    "|",
                    (
                        "order_partner_id",
                        "child_of",
                        unquote("partner_id if partner_id else []"),
                    ),
                    (
                        "order_id.partner_shipping_id",
                        "child_of",
                        unquote("partner_id if partner_id else []"),
                    ),
                    "|",
                    ("order_partner_id", "=?", unquote("partner_id")),
                    ("order_id.partner_shipping_id", "=?", unquote("partner_id")),
                    "|",
                    ("order_partner_id", "=?", unquote("project_partner_id")),
                    (
                        "order_id.partner_shipping_id",
                        "=?",
                        unquote("project_partner_id"),
                    ),
                    ("is_service", "=", True),
                    ("is_expense", "=", False),
                    ("state", "in", ["sale", "done"]),
                ],
            ]
        )
        return domain

    project_partner_id = fields.Many2one(
        "res.partner", string="Project Partner", related="project_id.partner_id"
    )
    delivery_partner_id = fields.Many2one(
        "res.partner",
        string="Delivery Partner",
        compute="_compute_delivery_partner",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id")
    def _compute_delivery_partner(self):
        """
        Partner (address) at which the physical operation take place.
        Might be different from the invoicing address.
        The standard field 'partner_id' is used to select the partner that must be invoiced.
        """
        for task in self:
            if task.partner_id and not task.delivery_partner_id:
                task.delivery_partner_id = task.partner_id

    def _get_partner_emails(self):
        """Get comma-separated attendee email addresses."""
        self.ensure_one()
        partners = self.partner_id | self.delivery_partner_id
        return ",".join([e for e in partners.mapped("email") if e])
