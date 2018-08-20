"""
API Interface Module
"""
#!/usr/bin/env python
# encoding: utf-8

import ujson as json
import utime
#from calendar import timegm
import urequests as requests
from classes.authentication.FlickAuth import FlickAuth
from classes.util.util import Util
from definitions import FLICK_PRICE_ENDPOINT, FLICK_DATA_STORE

util = Util();

class FlickApi(object):
    """ Flick Electric API Interface """

    def __init__(self, username, password, client_id, client_secret):
        AuthInstance = FlickAuth(username, password, client_id, client_secret)
        self.session = AuthInstance.getToken()
        self.getRawData()

    def __update(self, writeToFile=False):
        """ Pull Updates From Flick Servers"""

        print("getting the latest price")
        headers = {
          "Authorization": "Bearer %s" % self.session["id_token"]
        }
        req = requests.get(FLICK_PRICE_ENDPOINT, headers=headers)
        if req.status_code is not 200:
          # If we don't get a success response, we raise an exception.
          raise Exception({
            "status": req.status_code,
            "message": req.text
          })
        # A 200OK response will contain the JSON payload.
        # TODO: Create Exception Handler to catch failed json.load.
        response = json.loads(req.text)
        self.data = response
        return response


    # def __getUpdateTime(self, update, isEpoch):
    #     """ Gets the prev/next update time """
    #     if isEpoch is True:
    #         pattern = "%Y-%m-%dT%H:%M:%SZ"
    #         utc_time = time.strptime(update, pattern)
    #         epoch = timegm(utc_time)
    #         return epoch
    #     return update

    def getRawData(self, writeToFile=False):
        """ Public method to get pricing data """
        pricing = False
        if not pricing:
          pricing = self.__update(writeToFile)
        self.data = pricing
        return self.data

    def getPricePerKwh(self):
        """ Get's the pure price per kwh as a number"""
        return self.data["needle"]["price"]

    # def getPriceBreakdown(self):
    #     """ Get the price, broken down into it's constituent parts"""
    #     charges = 0.0
    #     spotPrice = 0.0
    #     for item in self.data["needle"]["components"]:
    #       if item["charge_method"] == "kwh":
    #         charges += float(item["value"])
    #       elif item["charge_method"] == "spot_price":
    #         spotPrice = float(item["value"])
    #
    #     response = {};
    #     response["charges"] = charges
    #     response["spotPrice"] = spotPrice
    #     return response
