#!/usr/bin/env python3
"""
Amazon Product Advertising API Example from:
http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html
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
import xmltodict

ENDPOINT = 'http://webservices.amazon.com/onca/xml'

def url_encode(word):
    """
    cleans word for url encoding
    """
    return urllib.parse.quote_plus(word.replace(' ', '_'))

def build_item_search_querystring(keywords, brand, search_index):
    """
    builds canonical querystring
    """
    if search_index is None:
        search_index = "All"

    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y-%m-%dT%H:%M:%SZ')
    # url encode date format: YYYY-MM-DD'T'HH:MM:SS'Z'
    amzdate = urllib.parse.quote_plus(amzdate)
    response_group = ["Images", "ItemAttributes"]
    response_group = url_encode(','.join(response_group))
    canonical_querystring = (
        "AWSAccessKeyId={}&AssociateTag={}&Availability=Available&"
        .format(ACCESS_KEY_ID, MY_ASSOCIATE_TAG)
    )
    if brand is not None:
        brand = url_encode(brand)
        canonical_querystring += 'Brand={}&'.format(brand)
    if keywords is not None:
        keywords = url_encode(','.join(keywords))
        canonical_querystring += 'Keywords={}&'.format(keywords)
    canonical_querystring += (
        "Operation=ItemSearch&ResponseGroup={}&SearchIndex={}&"
        "Service=AWSECommerceService&Timestamp={}&Version=2013-08-01"
        .format(response_group, search_index, amzdate)
    )
    return canonical_querystring

def build_canonical_request(canonical_querystring):
    """
    builds canonical request for Product Advertising
    http://webservices.amazon.com/onca/xml?
    """
    method = 'GET'
    host = 'webservices.amazon.com'
    canonical_uri = '/onca/xml'
    # create full canonical request based on previously set variables
    canonical_request = (
        "{}\n{}\n{}\n{}"
        .format(method, host, canonical_uri, canonical_querystring)
    )
    return canonical_request

def build_amazon_signature(canonical_request):
    """
    creates amazon signature based on canonical request and API credentials
    """
    # create signature
    signature = base64.b64encode(hmac.new(
        SECRET_ACCESS_KEY.encode('utf-8'),
        canonical_request.encode('utf-8'),
        hashlib.sha256
    ).digest()).decode("utf-8")
    return signature

def item_search(keywords=None, brand=None, search_index=None):
    """
    type(keywords) = list, []
    makes request to amazon product advertising api and returns request
    """
    if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY, MY_ASSOCIATE_TAG]) is False:
        print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
        return None
    if any([keywords, brand]) is False:
        print("Please provide at least a keyword or brand search value",
              file=sys.stderr)
        return None
    canonical_querystring = build_item_search_querystring(
        keywords, brand, search_index
    )
    canonical_request = build_canonical_request(canonical_querystring)
    signature = build_amazon_signature(canonical_request)
    # add signature to canonical query string
    canonical_querystring += (
        "&Signature={}".format(urllib.parse.quote_plus(signature))
    )
    request_url = "{}?{}".format(ENDPOINT, canonical_querystring)
    print('-------------- REQUEST URL ----------------')
    print(request_url)
    response = requests.get(request_url)
    if response.status_code != 200:
        print("There was an error in the request", file=sys.stderr)
        print("Status Code: {}".format(response.status_code), file=sys.stderr)
        print(response.text)
        return None
    return response

def build_item_lookup_querystring(asin=None):
    """
    builds canonical querystring
    """
    if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY, MY_ASSOCIATE_TAG]) is False:
        print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
        return None
    if asin is None:
        return None
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y-%m-%dT%H:%M:%SZ')
    # url encode date format: YYYY-MM-DD'T'HH:MM:SS'Z'
    amzdate = urllib.parse.quote_plus(amzdate)
    response_group = ["Images", "ItemAttributes"]
    response_group = url_encode(','.join(response_group))
    canonical_querystring = (
        "AWSAccessKeyId={}&AssociateTag={}&Availability=Available&"
        "Condition=All&IdType=ASIN&ItemId={}&Operation=ItemLookup&"
        "ResponseGroup={}&Service=AWSECommerceService&"
        "Timestamp={}".format(
            ACCESS_KEY_ID, MY_ASSOCIATE_TAG, asin, response_group, amzdate
        )
    )
    return canonical_querystring

def item_lookup(asin):
    """
    amazon API to search for item lookup based on ASIN #
    """
    canonical_querystring = build_item_lookup_querystring(asin)
    canonical_request = build_canonical_request(canonical_querystring)
    signature = build_amazon_signature(canonical_request)

    # add signature to canonical query string
    canonical_querystring += (
        "&Signature={}".format(urllib.parse.quote_plus(signature))
    )
    request_url = "{}?{}".format(ENDPOINT, canonical_querystring)
    response = requests.get(request_url)
    if response.status_code != 200:
        print("There was an error in the request", file=sys.stderr)
        print('-------------- REQUEST URL ----------------')
        print(request_url)
        print("Status Code: {}".format(response.status_code), file=sys.stderr)
        print(response.text)
        return None
    return response

def do_handle_amazon_search_item(item):
    """
    prints amazon response item from items search
    ItemLinks
    """
    amazon_object = {}
    for key, val in item.items():
        if key == "ASIN":
            amazon_object["ASIN"] = val
        elif key == "DetailPageURL":
            amazon_object["Detail Page URL"] = val
        elif key == "ItemLinks":
            itemlink = val.get("ItemLink")
            for link_item in itemlink:
                if link_item.get("Description") == "Technical Details":
                    amazon_object["Technical Details"] = link_item.get("URL")
        elif key == "LargeImage":
            amazon_object["Large Image"] = val.get("URL")
        elif key == "ItemAttributes":
            amazon_object["Title"] = val.get("Title")
            list_price = val.get("ListPrice")
            trade_in = val.get("TradeInValue")
            if list_price:
                amazon_object["Price"] = list_price.get("FormattedPrice")
            elif trade_in:
                amazon_object["Price"] = trade_in.get("FormattedPrice")
            else:
                amazon_object["Price"] = "No Price"
    return amazon_object

def response_is_valid(xml_dict):
    """
    checks if response has errors, and if so, handles that
    """
    item_response = xml_dict.get("ItemSearchResponse")
    if item_response is None:
        item_response = xml_dict.get("ItemLookupResponse")
    request = (
        item_response.get("Items").get("Request")
    )
    errors = request.get("Errors")
    if errors is None:
        return True
    message = errors.get("Error").get("Message")
    return {"ERROR": message}


def item_lookup_response_handler(response):
    """
    handles single item search response
    """
    xml_dict = xmltodict.parse(response.text)
    valid = response_is_valid(xml_dict)
    if valid is not True:
        return [valid]
    search_item = xml_dict.get('ItemLookupResponse').get("Items").get("Item")
    amazon_object = do_handle_amazon_search_item(search_item)
    return [amazon_object]


def item_search_response_handler(response):
    """
    parses and prints items from item search response
    """
    # convert xml to python objects
    xml_dict = xmltodict.parse(response.text)
    valid = response_is_valid(xml_dict)
    if valid is not True:
        return [valid]
    search_items = xml_dict.get("ItemSearchResponse").get("Items").get("Item")
    amazon_objects = []
    for item in search_items:
        amazon_object = do_handle_amazon_search_item(item)
        amazon_objects.append(amazon_object)
    return amazon_objects


if __name__ == "__main__":
    """
    MAIN APP
    """
    print(
        "Usage:\n"
        "import amazon_api\n"
        "amazon_api.item_search(keywords, brand, search_index)\n"
        "amazon_api.item_lookup(asin)"
    )
