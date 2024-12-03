import requests
from odoo import _
from odoo.exceptions import UserError


class PostSaleInventory:
    """
    A wrapper around the bang-olufsen.
    """

    def __init__(self, company, url, time_between_requests=0.6):
        """
        Args:
            company (Odoo record): A company record.
            url (str): The URL used to send the request.
            time_between_requests (float): Time in seconds between requests to
                the API to prevent spam. Default is 0.5 to prevent calls
                exceeding the 600 per 5 minutes limit.
        """
        if not company.b_and_o_api_active:
            raise UserError(_("B&O API is not actviated for this company %s.") % company.name)
        if not company.b_and_o_api_key:
            raise UserError(_("B&O API key is missing for company %s.") % company.name)
        self.key = company.b_and_o_api_key
        self.url = url
        self.time_between_requests = time_between_requests
        self.last_request_timestamp = None


    def post_data(self, body):
        """
        Posting data
        :param body: Data to send
        :return: http response
        """
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.key,
        }
        try:
            response = requests.post(
                self.url,
                json=body,
                headers=headers,
            )
            return response
        except Exception as e:
            raise UserError(f"Received Exception while calling api: {e}")
