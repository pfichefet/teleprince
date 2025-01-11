from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_fold = fields.Boolean(string="Folded Stage", related="stage_id.fold")
    opportunity_id = fields.Many2one("crm.lead", string="Opportunity")
    is_pre_visit_task = fields.Boolean(string="Is Pre-Visit Task", readonly=True)

    def action_fsm_validate(self, stop_running_timers=False):
        """
        Override method.
        The opportunity linked to the task move into the pre-visit done stage.
        """
        res = super().action_fsm_validate(stop_running_timers=stop_running_timers)
        for task in self:
            if task.is_pre_visit_task:
                pre_visit_done_crm_stage = self.env["crm.stage"].search([("is_pre_visit_done_stage", "=", True)], limit=1)
                if pre_visit_done_crm_stage and self.opportunity_id:
                    self.opportunity_id.stage_id = pre_visit_done_crm_stage
        return res
