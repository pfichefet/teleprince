from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    active = fields.Boolean(string="Active", default=True)
    is_pre_visit_stage = fields.Boolean(string="Pre-Visit Stage", help="Stage when the pre-visit has been scheduled.")
    is_pre_visit_done_stage = fields.Boolean(string="Pre-Visit Done Stage", help="Stage when the pre-visit stage has been done.")
