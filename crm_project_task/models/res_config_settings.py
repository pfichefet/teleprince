from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pre_visit_project_id = fields.Many2one("project.project", string="Pre-Visit Project", related="company_id.pre_visit_project_id", readonly=False)
