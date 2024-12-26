from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_fold = fields.Boolean(string="Folded Stage", related="stage_id.fold")
    opportunity_id = fields.Many2one("crm.lead", string="Opportunity")
    is_pre_visit_task = fields.Boolean(string="Is Pre-Visit Task", readonly=True)

    def pre_visit_done(self):
        """
        Method called by a button to close a pre visit task.
        The opportunity linked to the task move into the pre-visit done stage.
        """
        self.ensure_one()
        if self.is_pre_visit_task:
            done_stage = self.env['project.task.type'].search([('project_ids', 'in', self.project_id.id), ('fold', '=', True)], limit=1)
            if done_stage:
                self.stage_id = done_stage
            pre_visit_done_crm_stage = self.env["crm.stage"].search([("is_pre_visit_done_stage", "=", True)], limit=1)
            if pre_visit_done_crm_stage and self.opportunity_id:
                self.opportunity_id.stage_id = pre_visit_done_crm_stage
