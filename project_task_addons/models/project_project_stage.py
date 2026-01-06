from odoo import fields, models


class ProjectStage(models.Model):
    _inherit = "project.project.stage"

    display_project_fsm_app = fields.Boolean(
        string="Is Project Open",
        default=True,
        help="Indicates whether the project appears in " \
        "the dropdown list of an FSM tasks.",
    )