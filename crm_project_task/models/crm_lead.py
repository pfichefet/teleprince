from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many("project.task", "opportunity_id", string="Tasks")
    tasks_count = fields.Integer(string='Tasks', compute='_compute_tasks_ids', groups="project.group_project_user")

    @api.depends('task_ids')
    def _compute_tasks_ids(self):
        for lead in self:
            lead.tasks_count = len(lead.task_ids)

    def action_view_tasks(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('project.action_view_all_task')
        action.update({
            'name': _('Tasks'),
            'domain': [
                ('id', 'in', self.task_ids.ids),
            ],
        })
        return action

    def _prepare_pre_visit_task_values(self):
        """
        Prepare a dictionary of values to create a project task.
        """
        self.ensure_one()
        company = self.company_id or self.env.company
        pre_visit_project = company.pre_visit_project_id
        if not pre_visit_project:
            raise UserError(_('Please set a pre-visit project in the CRM settings.'))
        return {
            "name": _("Pre-Visit: %s") % self.name,
            "project_id": pre_visit_project.id,
            "partner_id": self.partner_id.id,
            "company_id": company.id,
            "is_pre_visit_task": True,
            "opportunity_id": self.id,
        }

    def create_pre_visit_task(self):
        """
        Method called by a button to create a pre visit task linked to the opportunity.
        Return the form view of the task.
        """
        self.ensure_one()
        values = self._prepare_pre_visit_task_values()
        task = self.env["project.task"].create(values)
        pre_visit_stage = self.env["crm.stage"].search([("is_pre_visit_stage", "=", True)], limit=1)
        if pre_visit_stage:
            self.stage_id = pre_visit_stage
        view = self.env.ref('project.view_task_form2')
        return {
            'name': _('Pre-Visit Task'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': task.id,
        }
