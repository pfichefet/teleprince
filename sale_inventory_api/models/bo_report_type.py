from odoo import models, fields, _


class BOReportType(models.Model):
    _name = "bo.report.type"
    _description = "B&O report type"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    technical_name = fields.Char(string='Technical Name', required=True)
    url_endpoint = fields.Char(string='URL Endpoint', required=True)
    url_no_data_endpoint = fields.Char(string='URL NoData Endpoint')
