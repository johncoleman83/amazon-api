#!/usr/bin/env python3
"""
Amazon Product Advertising API Example from:
http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html

canonical_querystring = 'AWSAccessKeyId={}&'.format(ACCESS_KEY_ID)
canonical_querystring += 'AssociateTag={}&'.format(MY_ASSOCIATE_TAG)
canonical_querystring += 'ItemId=0679722769&'
canonical_querystring += 'Operation=ItemLookup&'
canonical_querystring += 'ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews'
canonical_querystring += 'Service=AWSECommerceService'
canonical_querystring += 'Timestamp={}&'.format(amzdate)
canonical_querystring += 'Version=2013-08-01'

expected result from EXAMPLE hash:
signature = 'j7bZM0LXZ9eXeZruTqWm2DIvDYVUU3wxPPpp+iXxzQc='
"""
from authentication import ACCESS_KEY_ID, SECRET_ACCESS_KEY, MY_ASSOCIATE_TAG
import base64
import datetime
import hashlib
import hmac
import os
import requests
import sys
import urllib.parse
import xmltodict, json


def build_canonical_querystring(keywords, brand, search_index):
    """
    builds canonical querystring
    """
    if search_index is None:
        search_index = "All"

    keywords = urllib.parse.quote_plus(','.join(keywords))
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y-%m-%dT%H:%M:%SZ')
    # url encode date format: YYYY-MM-DD'T'HH:MM:SS'Z'
    amzdate = urllib.parse.quote_plus(amzdate)

    canonical_querystring = (
        "AWSAccessKeyId={}&AssociateTag={}&Availability=Available&"
        .format(ACCESS_KEY_ID, MY_ASSOCIATE_TAG)
    )
    if brand is not None:
        canonical_querystring += 'Brand={}&'.format(brand)
    if keywords is not None:
        canonical_querystring += 'Keywords={}&'.format(keywords)
    canonical_querystring += (
        "Operation=ItemSearch&SearchIndex={}&Service=AWSECommerceService&"
        "Timestamp={}&Version=2013-08-01".format(search_index, amzdate)
    )
    return canonical_querystring

def amazon_prod_add_api_search(keywords=None, brand=None, search_index=None):
    """
    type(keywords) = list, []
    makes request to amazon product advertising api and returns request
    """
    if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY, MY_ASSOCIATE_TAG]) is False:
        print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
        return None
    if any([keywords is not None, brand is not None]) is False:
        print("Please provide at least a keyword or brand search value",
              file=sys.stderr)
        return None
    method = 'GET'
    service = 'AWSECommerceService'
    host = 'webservices.amazon.com'
    canonical_uri = '/onca/xml'
    endpoint = 'http://webservices.amazon.com/onca/xml'
    canonical_querystring = build_canonical_querystring(
        keywords, brand, search_index
    )
    # create full canonical request based on previously set variables
    canonical_request = (
        "{}\n{}\n{}\n{}"
        .format(method, host, canonical_uri, canonical_querystring)
    )
    # create signature
    signature = base64.b64encode(hmac.new(
        SECRET_ACCESS_KEY.encode('utf-8'),
        canonical_request.encode('utf-8'),
        hashlib.sha256
    ).digest()).decode("utf-8")
    # add signature to canonical query string
    canonical_querystring += (
        "&Signature={}".format(urllib.parse.quote_plus(signature))
    )
    request_url = "{}?{}".format(endpoint, canonical_querystring)
    print('-------------- REQUEST URL ----------------')
    print(request_url)
    response = requests.get(request_url)
    if response.status_code != 200:
        print("There was an error in the request", file=sys.stderr)
        print("Status Code: {}".format(response.status_code), file=sys.stderr)
        print(response.text)
        return None
    return response

def do_amazon_search_item(item):
    """
    prints amazon response item from items search
    ItemLinks
    """
    for key, val in item.items():
        if key == "ASIN":
            asin = val
            print("Product ASIN: {}".format(asin))
        elif key == "DetailPageURL":
            detailpageurl = val
            print("Page URL: {}".format(detailpageurl))
        elif key == "ItemLinks":
            itemlink = val.get("ItemLink")
            for link_item in itemlink:
                print("{} : {}".format(link_item.get("Description"),
                                       link_item.get("URL"))
                )

def search_response_handler(response):
    """
    parses and prints items from item search response
    """
    # convert xml to python objects
    xml_dict = xmltodict.parse(response.text)
    search_response = xml_dict.get("ItemSearchResponse")
    search_items = search_response.get("Items").get("Item")
    for item in search_items:
        do_amazon_search_item(item)


if __name__ == "__main__":
    """
    MAIN APP
    """
    print(
        """Usage:
import amazon_api
amazon_api.amazon_prod_add_api_search(keywords, brand, search_index)"""
    )
