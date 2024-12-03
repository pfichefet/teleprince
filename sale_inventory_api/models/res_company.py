from odoo import fields, models, _
from odoo.exceptions import UserError

class Company(models.Model):
    _inherit = "res.company"

    b_and_o_api_active = fields.Boolean(string="B&O Active API")
    b_and_o_api_environment = fields.Selection(
        [('test', 'Test'), ('prod', 'Production')], string="B&O Environment", default="test",
    )
    b_and_o_api_key = fields.Char(string="B&O API Key")
    b_and_o_api_id = fields.Char(string="B&O API ID")
    b_and_o_api_store = fields.Integer(string="B&O API Store")
    b_and_o_api_start_date = fields.Date(string="B&O API Start Date", help="Odoo will send Sale data from this date")
    b_and_o_api_time_delta = fields.Integer(string="Time Delta (in days)", default=30,
                                            help="Specify the number of days Odoo should wait before sending sales data.\n"
                                                 "For example, if a sales order is dated as day X, Odoo will send the data on day X + time_delta.")

    def get_api_bo_url(self):
        """
        Return the base URL depending on the environment set.
        """
        self.ensure_one()
        if self.b_and_o_api_environment == "test":
            url = self.env['ir.config_parameter'].sudo().get_param('b_and_o_test_url')
        elif self.b_and_o_api_environment == "prod":
            url = self.env['ir.config_parameter'].sudo().get_param('b_and_o_base_url')
        else:
            raise UserError(_("B&O API Environment is not supported (company: %s)") % self.name)
        if not url:
            raise UserError(_("B&O API URL is not set"))
        return url
