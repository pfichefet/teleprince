from odoo import api, Command, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    task_ids = fields.One2many("project.task", "calendar_event_id", string="Tasks")
    task_id = fields.Many2one("project.task", string="Task", compute="_compute_task_id")
    project_id = fields.Many2one("project.project", string="Project")
    task_partner_id = fields.Many2one("res.partner", string="Customer")

    @api.depends('partner_ids')
    @api.depends_context('uid')
    def _compute_user_can_edit(self):
        # Overwrite the standard method.
        # Let anyone modify any event.
        for event in self:
            event.user_can_edit = True

    @api.depends("privacy", "user_id", "project_id")
    def _compute_display_name(self):
        """
        If an event is link to a project display the project's name
        """
        super()._compute_display_name()
        for event in self.filtered(lambda e: e.project_id):
            event.display_name = f"{event.sudo().project_id.name}: {event.display_name}"

    @api.depends("task_ids")
    def _compute_task_id(self):
        """
        Return the first task linked to this event
        """
        for event in self:
            if event.task_ids:
                event.task_id = event.task_ids[0]
            else:
                event.task_id = False

    def _prepare_project_task_values(self):
        """
        Prepare a dictionary of values to create a project task
        """
        self.ensure_one()
        values = {
            "name": f"{self.name}",
            "description": self.description,
            "partner_id": self.task_partner_id.id if self.task_partner_id else False,
            "project_id": self.project_id.id,
            "planned_date_begin": self.start,
            "date_deadline": self.stop,
            "user_ids": [Command.set(self.partner_ids.mapped("user_ids.id"))],
            "calendar_event_id": self.id,
        }
        return values

    def create_project_task(self):
        """
        If a project is set on a calendar event, create a new task
        """
        list_values = []
        for event in self:
            if event.project_id:
                list_values.append(event._prepare_project_task_values())
        self.env["project.task"].with_context(task_event=True).create(list_values)

    @api.model_create_multi
    def create(self, vals_list):
        """
        If a project is set on a calendar event, create a new task
        """
        events = super(CalendarEvent, self.with_context(task_event=True)).create(
            vals_list
        )
        # We check the context to avoid recursive loop
        if not self.env.context.get("task_event", False):
            events.create_project_task()
        return events

    def write(self, vals):
        """
        When modification are applied to the calendar event apply the same changes on the project task
        """
        event_without_tasks = self.filtered(lambda e: not e.task_ids)
        res = super(CalendarEvent, self.with_context(task_event=True)).write(vals)
        if any(
            [
                field in vals
                for field in [
                    "name",
                    "project_id",
                    "description",
                    "start",
                    "stop",
                    "partner_ids",
                    "task_partner_id",
                ]
            ]
        ) and not self.env.context.get("task_event", False):
            for event in self:
                if event.task_ids:
                    values = event._prepare_project_task_values()
                    event.task_ids.with_context(task_event=True).write(values)
        # If an existing calendar event is link for the first time to a project create a new task
        if (
            "project_id" in vals
            and vals.get("project_id", False)
            and event_without_tasks
        ):
            event_without_tasks.with_context(task_event=True).create_project_task()
        # If we unlink a calendar event from its project we delete the task
        if "project_id" in vals and not vals.get("project_id", False):
            tasks = self.task_ids
            if tasks:
                tasks.with_context(task_event=True).unlink()
        return res

    def unlink(self):
        """
        If we delete a calendar event then we delete its corresponding task
        """
        if self.task_ids and not self.env.context.get("task_event", False):
            self.task_ids.with_context(task_event=True).unlink()
        return super().unlink()
