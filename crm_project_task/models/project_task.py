from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_fold = fields.Boolean(string="Folded Stage", related="stage_id.fold")
    opportunity_id = fields.Many2one("crm.lead", string="Opportunity")
    is_pre_visit_task = fields.Boolean(string="Is Pre-Visit Task", readonly=True)

    # @api.depends('worksheet_count', 'allow_worksheets')
    # def _compute_display_conditions_count(self):
    #     """
    #     Overwrite standard method
    #     Always print the Task Report even if no TS or no Worksheets are made.
    #     """
    #     self.update({
    #         'display_satisfied_conditions_count': 1,
    #     })

    def action_fsm_validate(self, stop_running_timers=False):
        """
        Override method.
        The opportunity linked to the task move into the pre-visit done stage.
        """
        res = super().action_fsm_validate(stop_running_timers=stop_running_timers)
        closed_stage_by_project = {
            project.id: project.type_ids.filtered(lambda stage: stage.fold)[:1]
            or project.type_ids[-1:]
            for project in self.project_id
        }
        for task in self:
            if task.is_pre_visit_task:
                pre_visit_done_crm_stage = self.env["crm.stage"].search(
                    [("is_pre_visit_done_stage", "=", True)], limit=1
                )
                if pre_visit_done_crm_stage and task.opportunity_id:
                    task.opportunity_id.stage_id = pre_visit_done_crm_stage
            # determine closed stage for task
            closed_stage = closed_stage_by_project.get(task.project_id.id)
            if closed_stage:
                task.stage_id = closed_stage
        return res
