import json
from datetime import timedelta
import logging
from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.sale_inventory_api.API.post_sale_inventory import PostSaleInventory

_logger = logging.getLogger(__name__)


class BOReport(models.Model):
    _name = "bo.report"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "B&O report"
    _order = "date_start desc, id"

    name = fields.Char(string='Name', required=True, readonly=True, default=_('New'))
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    report_type_id = fields.Many2one("bo.report.type", string='Report Type', required=True)
    report_type_technical_name = fields.Char(string='Report Type Technical Name', related='report_type_id.technical_name')
    status = fields.Selection([('draft', 'Draft'), ('error', 'Error'), ('correct', 'Correct'), ('sent', 'Sent'), ('fail', 'Fail')],
                              string="Status",
                              required=True,
                              readonly=True,
                              tracking=True,
                              default='draft')
    report_line_sale_ids = fields.One2many('bo.report.line.sale', 'report_id', string='Report Sale Lines')
    report_line_quant_ids = fields.One2many('bo.report.line.quant', 'report_id', string='Report Inventory Lines')
    body = fields.Text(string="Data", readonly=True)
    url = fields.Char(string="URL", readonly=True)
    error_msg = fields.Text(string="Error", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.constrains('date_start', 'date_end')
    def no_date_overlap(self):
        """
        Date of a B&O report cannot overlap!
        """
        for report in self:
            overlap_report = self.get_bo_report_overlap(report.date_start, report.date_end, report.report_type_id.id, report.company_id.id, report.id)
            if overlap_report:
                raise ValidationError(_("At least two B&O reports overlap each other. %s") % overlap_report.mapped('name'))

    @api.model
    def get_bo_report_overlap(self, date_start, date_end, report_type_id, company_id, report_id=False):
        """
        Return B&O report that match the given parameters.
        Used to find B&O report that would be in conflict with the one we are creating.
        """
        domain = [('date_start', '<=', date_end),
                  ('date_end', '>=', date_start),
                  ('report_type_id', '=', report_type_id),
                  ('company_id', '=', company_id),]
        if report_id:
            domain.append(('id', '!=', report_id))
        overlap_report = self.env['bo.report'].search(domain)
        return overlap_report

    @api.model_create_multi
    def create(self, vals_list):
        """
        Generate a Name depending on the sequence set.
        """
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_start'])
                ) if 'date_start' in vals else None
                context = {"ir_sequence_date": seq_date.strftime("%Y-%m-%d")} if seq_date else {}
                vals['name'] = self.env['ir.sequence'].with_context(context).next_by_code(
                    'bo.report', sequence_date=seq_date) or _("New")
        return super().create(vals_list)

    def generate_sale_data(self):
        """
        Generate data to send to B&O based on the sales.
        """
        self.ensure_one()
        bo_report_line = self.env['bo.report.line.sale'].search([('report_id', '!=', self.id)])
        sale_lines_in_report = bo_report_line.sale_line_id
        sale_order_lines = self.env['sale.order.line'].search([
            ('order_id.state', 'in', ['sale', 'done']),
            ('product_id', '!=', False),
            ('product_id.is_api_b_and_o_compliant', '=', True),
            ('qty_invoiced', '>', 0),
            ('invoice_date', '!=', False),
            ('invoice_date', '>=', self.date_start),
            ('invoice_date', '<=', self.date_end),
            ('id', 'not in', sale_lines_in_report.ids),
            ('company_id', '=', self.company_id.id)])
        list_values = [Command.clear()]
        for sale_line in sale_order_lines:
            sn_values = sale_line.prepare_bo_report_line(self)
            list_values.extend([Command.create(values) for values in sn_values])
        self.sudo().write({"report_line_sale_ids": list_values})

    def generate_inventory_data(self):
        """
        Generate data to send to B&O based on the inventory.
        """
        self.ensure_one()
        quants = self.env['stock.quant'].search([('inventory_quantity_set', '=', False),
                                                 ('company_id', '=', self.company_id.id),
                                                 ('product_id.active', '=', True),
                                                 ('product_id.is_api_b_and_o_compliant', '=', True),
                                                 ('quantity', '>', 0),
                                                 ('location_id.usage', 'in', ['internal', 'transit'])])
        list_values = [Command.clear()]
        for quant in quants:
            values = quant.prepare_bo_report_line(self)
            list_values.append(Command.create(values))
        self.sudo().write({"report_line_quant_ids": list_values})

    def generate_data(self):
        """
        Search in the database for data to send.
        """
        for report in self.filtered(lambda r: r.status != 'sent'):
            if report.report_type_technical_name == "Sell-Out Sales":
                report.generate_sale_data()
            elif report.report_type_technical_name == "Sell-Out Inventory":
                report.generate_inventory_data()
            report.sudo().status = 'draft'

    def check_data_validity(self):
        """
        Check the validity of the date before sending them.
        """
        for report in self.filtered(lambda r: r.status != 'sent'):
            for line in report.report_line_sale_ids:
                line.check_data_validity()
            for line in report.report_line_quant_ids:
                line.check_data_validity()
            if any(line.error for line in report.report_line_sale_ids) or any(line.error for line in report.report_line_quant_ids):
                report.sudo().status = 'error'
            else:
                report.sudo().status = 'correct'

    def prepare_json_body(self):
        """
        Prepare the body that will be sent through API REST request.
        """
        self.ensure_one()
        body = {
            "fileTypeName": self.report_type_technical_name,
        }
        data = []
        lines = self.env['bo.report.line.abstract']
        if self.report_type_technical_name == "Sell-Out Sales":
            lines = self.report_line_sale_ids
        elif self.report_type_technical_name == "Sell-Out Inventory":
            lines = self.report_line_quant_ids
        for line in lines:
            data.extend(line.prepare_api_json_values())
        if data:
            body.update({"data": data})
        else:
            body.update({
                "startDate": self.date_start.strftime("%Y-%m-%d"),
                "endDate": self.date_end.strftime("%Y-%m-%d"),
            })
        self.sudo().body = json.dumps(body)
        return body

    def send_data(self):
        """
        Send the data to B&O.
        """
        self.check_data_validity()
        for report in self.filtered(lambda r: r.status == 'correct'):
            body = report.prepare_json_body()
            base_url = report.company_id.get_api_bo_url()
            if body.get("data", False):
                url_endpoint = report.report_type_id.url_endpoint
            else:
                url_endpoint = report.report_type_id.url_no_data_endpoint
            if not report.company_id.b_and_o_api_id:
                raise UserError(_("B&O API ID is missing for company %s.") % report.company_id.name)
            api_id = report.company_id.b_and_o_api_id
            url = url_endpoint.format(baseUrl=base_url, apiId=api_id)
            report.sudo().url = url
            post_sale_inventory_api = PostSaleInventory(
                report.company_id, url,
            )
            try:
                response = post_sale_inventory_api.post_data(body)
                if response.status_code != 200:
                    error_message = response.json().get("message", "No message provided")
                    report.error_msg = error_message
                    report.sudo().status = 'fail'
            except Exception as e:
                report.error_msg = e
                report.sudo().status = 'fail'
        return True

    @api.model
    def send_data_by_cron(self, bo_report_type_name):
        """
        Generate one B&O report par week.
        We start with the week set in the settings and end at today - the time delta configured.
        """
        # Try to send unsent report
        existing_bo_reports = self.env['bo.report'].sudo().search([('report_type_id.technical_name', '=', bo_report_type_name), ('status', '!=', 'sent')])
        existing_bo_reports.send_data()
        companies = self.env['res.company'].sudo().search([('b_and_o_api_active', '=', True)])
        report_type = self.env['bo.report.type'].search([('technical_name', '=', bo_report_type_name)], limit=1)
        if not report_type:
            raise UserError(_("No report type found with technical name %s.") % bo_report_type_name)
        for company in companies:
            if bo_report_type_name == "Sell-Out Sales":
                start_date = company.b_and_o_api_start_date
                if start_date:
                    # Create one sale report per week until we reach the end date.
                    end_date = fields.Date.today() - timedelta(days=company.b_and_o_api_time_delta)
                    current_date = start_date
                    while current_date <= end_date:
                        days_until_sunday = 6 - current_date.weekday()
                        end_of_week = current_date + timedelta(days=days_until_sunday)
                        values = {'date_start': current_date, 'date_end': end_of_week, 'company_id': company.id, 'report_type_id': report_type.id}
                        self.sudo().generate_report(values)
                        current_date = end_of_week + timedelta(days=1)
                    # Save the date we reach, this way we will start from this point next time.
                    company.sudo().b_and_o_api_start_date = current_date
            elif bo_report_type_name == "Sell-Out Inventory":
                today = fields.Date.today()
                days_until_sunday = 6 - today.weekday()
                end_of_week = today + timedelta(days=days_until_sunday)
                start_week = today - timedelta(days=today.weekday())
                values = {'date_start': start_week, 'date_end': end_of_week, 'company_id': company.id, 'report_type_id': report_type.id}
                self.sudo().generate_report(values)
            else:
                raise UserError(_("Report type technical name unsupported %s." % bo_report_type_name))

    @api.model
    def generate_report(self, values):
        """
        Try to generate a B&O report, and to send its data.
        This method purpose it to be called by a CRON.
        """
        try:
            overlap_report = self.get_bo_report_overlap(values['date_start'], values['date_end'], values['report_type_id'], values['company_id'])
            if not overlap_report:
                bo_report = self.env['bo.report'].create(values)
                bo_report.generate_data()
                bo_report.send_data()
            else:
                _logger.warning("At least two B&O reports overlap each other. %s" % overlap_report.mapped('name'))
        except Exception as e:
            _logger.warning("Failed to generate B&O report with those values: %s\n%s" % (values, e))
