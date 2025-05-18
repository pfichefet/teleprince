import odoo.models
from odoo import api, Command, fields, models

# Modify the display format
odoo.models.READ_GROUP_DISPLAY_FORMAT["day"] = "EEE, dd MMM yyyy"
PROJECT_TASK_READABLE_FIELDS = {
    "calendar_event_id",
}


class ProjectTask(models.Model):
    _inherit = "project.task"

    calendar_event_id = fields.Many2one("calendar.event", string="Event Calendar")

    @property
    def SELF_READABLE_FIELDS(self):
        return PROJECT_TASK_READABLE_FIELDS | super().SELF_READABLE_FIELDS

    def _prepare_calendar_event_values(self):
        """
        Prepare a dictionary of values to create a calendar event
        """
        self.ensure_one()
        values = {
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id.id,
            "task_partner_id": self.partner_id.id if self.partner_id else False,
            "start": self.planned_date_begin,
            "stop": self.date_deadline,
            "partner_ids": [Command.set(self.user_ids.mapped("partner_id.id"))],
        }
        return values

    def create_calendar_event(self):
        for task in self:
            if task.planned_date_begin and task.date_deadline and task.project_id:
                task.calendar_event_id = (
                    self.env["calendar.event"]
                    .with_context(task_event=True)
                    .create(task._prepare_calendar_event_values())
                )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create a calendar event link to each created tasks
        """
        tasks = super(ProjectTask, self.with_context(task_event=True)).create(vals_list)
        if not self.env.context.get("task_event", False):
            tasks.create_calendar_event()
        return tasks

    def write(self, vals):
        """
        When modification are applied to the task apply the same changes on the calendar event
        """
        res = super(ProjectTask, self.with_context(task_event=True)).write(vals)
        if any(
            [
                field in vals
                for field in [
                    "name",
                    "project_id",
                    "description",
                    "date_deadline",
                    "planned_date_begin",
                    "user_ids",
                    "partner_id",
                ]
            ]
        ) and not self.env.context.get("task_event", False):
            for task in self:
                if task.calendar_event_id:
                    values = task._prepare_calendar_event_values()
                    task.calendar_event_id.with_context(task_event=True).write(values)
                else:
                    task.create_calendar_event()
        return res

    def unlink(self):
        """
        Is the task is deleted, delete its calendar event if it exists
        """
        if self.calendar_event_id and not self.env.context.get("task_event", False):
            self.calendar_event_id.with_context(task_event=True).unlink()
        return super().unlink()
