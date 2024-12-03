import re
from odoo import api, fields, models, _


class BOReportLineAbstract(models.AbstractModel):
    _name = 'bo.report.line.abstract'
    _description = "B&O report line abstract"

    name = fields.Text(
        string="Description",
        compute='_compute_name',
        store=True, readonly=True, required=True, precompute=True)
    report_id = fields.Many2one("bo.report", string="B&O Report", readonly=True, ondelete='cascade')
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse", readonly=True)
    date = fields.Date(string="Date", required=True, readonly=True)
    product_id = fields.Many2one("product.product", string="Product", required=True, readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)
    uom_id = fields.Many2one("uom.uom", string="UOM", required=True, readonly=True)
    lot_id = fields.Many2one("stock.lot", string="Lot", domain="[('product_id', '=', product_id)]")
    company_id = fields.Many2one('res.company', string='Company', related='report_id.company_id')
    error = fields.Boolean(string="Error", readonly=True)
    error_msg = fields.Text(string="Error Message", readonly=True)

    @api.depends('product_id', 'lot_id')
    def _compute_name(self):
        """
        Compute the name of the line
        """
        for line in self:
            if line.lot_id:
                name = f"{line.product_id.display_name} - {line.lot_id.name}"
            else:
                name = f"{line.product_id.display_name}"
            line.name = name

    def check_data_validity(self):
        """
        Override method
        Ensure the validity of the data that we are about to send.
        """
        self.ensure_one()
        sku = self.product_id.default_code or ""
        match_product_ref = bool(re.match(r'^\d{1,10}$', sku))
        error = False
        error_msg = ""
        if not match_product_ref:
            error = True
            error_msg += _("The product identifier must be string that consists of only digits.\n"
                           "The length of the string must be between 1 and 10 characters (inclusive).")
        quantity = str(self.quantity)
        match_qty = bool(re.match(r'[-+]?\d+(.\d+)?', quantity))
        if not match_qty:
            error = True
            if error_msg:
                error_msg += "\n"
            error_msg += _("The quantity must a be a string.\n"
                           "May or may not have a sign (+ or -).\n"
                           "Must have at least one digit before the optional decimal point.\n"
                           "May or may not include a fractional part after the decimal point.")
        store_id = self.warehouse_id.store_identifier or self.company_id.b_and_o_api_store
        store_id = str(store_id) if store_id else ""
        match_store_id = bool(re.match(r'^\d+$', store_id))
        if not match_store_id:
            error = True
            if error_msg:
                error_msg += "\n"
            error_msg += _("You must defined a Store identifier on the warehouse %s.") % self.warehouse_id.name
        sn_name = self.lot_id.name or ""
        if sn_name:
            match_sn = bool(re.match(r'^\d{8}$', sn_name))
            if not match_sn:
                error = True
                if error_msg:
                    error_msg += "\n"
                error_msg += _("The SN must be string that consists of only digits.\n"
                               "The length of the string must be exactly 8 characters.")
        self.sudo().error = error
        self.sudo().error_msg = error_msg

    def prepare_api_json_values(self):
        """
        Prepare a dictionary that has as key a line ID and as values a dictionary that can be sent to B&O
        through the REST API.
        """
        self.ensure_one()
        list_values = []
        values = {
            "storeid": str(self.warehouse_id.store_identifier) if self.warehouse_id else str(self.company_id.b_and_o_api_store),
            "sku": self.product_id.default_code,
            "materialName": self.product_id.display_name,
            "storeName": self.warehouse_id.name,
            "unitofmeasure": self.uom_id.name,
        }
        if self.lot_id:
            values.update({
                "serialNumber": self.lot_id.name,
            })
        list_values.append(values)
        return list_values
