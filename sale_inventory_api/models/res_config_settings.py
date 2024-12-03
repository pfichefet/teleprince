from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    b_and_o_api_active = fields.Boolean(string="B&O API activate", related="company_id.b_and_o_api_active", readonly=False)
    b_and_o_api_key = fields.Char(string="API Key", related="company_id.b_and_o_api_key", readonly=False)
    b_and_o_api_id = fields.Char(string="API ID", related="company_id.b_and_o_api_id", readonly=False)
    b_and_o_api_environment = fields.Selection(
        string="B&O Environment", related="company_id.b_and_o_api_environment", readonly=False
    )
    b_and_o_base_url = fields.Char(string="Base URL", config_parameter="b_and_o_base_url")
    b_and_o_test_url = fields.Char(string="Test URL", config_parameter="b_and_o_test_url")
    b_and_o_api_store = fields.Integer(string="API Store", related="company_id.b_and_o_api_store", readonly=False)
    b_and_o_api_start_date = fields.Date(string="B&O API Start Date", related="company_id.b_and_o_api_start_date", readonly=False)
    b_and_o_api_time_delta = fields.Integer(string="Time Delta (in days)", related="company_id.b_and_o_api_time_delta", readonly=False)
