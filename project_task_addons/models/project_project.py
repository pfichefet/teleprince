from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    display_project_fsm_app = fields.Boolean(
        string="Is Project Open",
        related="stage_id.display_project_fsm_app",
        help="Indicates whether the project appears in " \
        "the dropdown list of an FSM tasks.",
    )
