import requests
import json
import datetime
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class PostSaleInventory:
    """A wrapper around the bang-olufsen.

    Attributes:
        sale_url (str): Base url for posting sales.
        inventory_url (str): Base url for posting inventory.

    """
    sale_test_url = "https://test.api.bang-olufsen.dk/posdata/v1-test/api/Sale"
    inventory_test_url = "https://test.api.bang-olufsen.dk/posdata/v1-test/api/Inventory"
    sale_prod_url = "https://api.bang-olufsen.dk/posdata/v1/api/Sale"
    inventory_prod_url = "https://api.bang-olufsen.dk/posdata/v1/api/Inventory"

    def __init__(self, key, environment, time_between_requests=0.6):
        print ("keyyyyyyyyyyyyyyyy", key)
        print ("environment", environment)
        """
        Args:
            key (str): The API key issued in the Bang olufsen API.
            time_between_requests (float): Time in seconds between requests to
                the API to prevent spam. Default is 0.5 to prevent calls
                exceeding the 600 per 5 minutes limit.
        """
        if not key:
            raise UserError("Please configure the B & O API in the company.")
        self.key = key
        self.time_between_requests = time_between_requests

        # : datetime: Timestamp instantiated as NoneType
        self.last_request_timestamp = None
        self.environment = environment

    def post_sale_data(self, payload):
        """
        Posting Sales data
        :param payload: Data
        :return: True
        """
        url = getattr(self, f'sale_{self.environment}_url')
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.key,
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
            )
            print ("response.status_code sale data", response.text)
            print ("\n", response.status_code)
            if response.status_code == 201:
                return response
            elif response.status_code == 500:
                _logger.info('payload', payload)
                return response
                raise UserError(f"Request could not be completed, error cause: API {response.reason}")
            else:
                raise UserError(f"Request could not be completed, error cause: {response.json()}")
            return response
        except Exception as e:
            raise UserError(f"Received Exception while calling api: {e}")

    def post_inventory_data(self, payload):
        """
        Posting Inventory data
        :param payload: Data
        :return: True
        """
        url = getattr(self, f'inventory_{self.environment}_url')
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.key,
        }

        # try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        print ("response.status_code Inventory>>>", response.status_code)
        if response.status_code == 201:
            return True
        else:
            raise UserError(f"Request could not be completed, error cause: {response.json()}")
