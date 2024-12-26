from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    pre_visit_project_id = fields.Many2one("project.project", string="Pre-Visit Project")
