#!/usr/bin/env python3
"""
This file contains AWS GET request templates from
http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
AWS Version 4 signing example - EC2 API (DescribeRegions)
"""
from authentication import ACCESS_KEY_ID, SECRET_ACCESS_KEY, MY_ASSOCIATE_TAG
import base64
import sys, os, base64, datetime, hashlib, hmac, urllib.parse
import requests

if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY]) is False:
    print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
    sys.exit()


# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y-%m-%dT%H:%M:%SZ') # Format date as YYYYMMDD'T'HHMMSS'Z'
method = 'GET'
service = 'AWSECommerceService'
host = 'webservices.amazon.com'
canonical_uri = '/onca/xml'
endpoint = 'http://webservices.amazon.com/onca/xml'


# Create the canonical query string. In this example, request

canonical_querystring = 'AWSAccessKeyId={}&'.format(ACCESS_KEY_ID)
canonical_querystring += "AssociateTag={}&".format(MY_ASSOCIATE_TAG)
canonical_querystring += 'Availability=Available&'
canonical_querystring += 'Brand=Lacoste&'
canonical_querystring += 'Keywords=shirts&'
canonical_querystring += 'Operation=ItemSearch&'
canonical_querystring += 'SearchIndex=FashionWomen&'
canonical_querystring += 'Service=AWSECommerceService&'
canonical_querystring += 'Timestamp={}&'.format(amzdate)
canonical_querystring += "Version=2013-08-01"

# create full canonical request
canonical_request = (
    "{}\n{}\n{}\n{}"
    .format(method, host, canonical_uri, canonical_querystring)
)

signature = base64.b64encode(hmac.new(
    SECRET_ACCESS_KEY.encode('utf-8'),
    canonical_request.encode('utf-8'),
    hashlib.sha256

).digest()).decode("utf-8")

canonical_querystring += (
    "&Signature={}".format(urllib.parse.quote_plus(signature))
)

# ************* SEND THE REQUEST *************
request_url = "{}?{}".format(endpoint, canonical_querystring)

print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print("Request URL = ", request_url)
r = requests.get(request_url)
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: {}\n'.format(r.status_code))
print(r.text)
