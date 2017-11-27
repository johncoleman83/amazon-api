#!/usr/bin/env python3
"""
This file contains AWS GET request templates from
http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
AWS Version 4 signing example - EC2 API (DescribeRegions)
"""
from authentication import ACCESS_KEY_ID, SECRET_ACCESS_KEY
import sys, os, base64, datetime, hashlib, hmac
import requests

if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY]) is False:
    print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
    sys.exit()

# ************* REQUEST VALUES *************
method = 'GET'
service = 'ec2'
host = 'ec2.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://ec2.amazonaws.com'
request_parameters = 'Action=DescribeRegions&Version=2013-10-15'

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    """
    hashes with hmac each component of Signature Key
    """
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    """
    creates signature key with hash from sign()
    """
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


# CREATE A CANONICAL REQUEST
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Create canonical URI--the part of the URI from domain to query string
# (use '/' if no path)
canonical_uri = '/'

# Create the canonical query string. In this example (a GET request),
# request parameters are in the query string. Query string values must
# be URL-encoded (space=%20). The parameters must be sorted by name.
canonical_querystring = request_parameters

# Create the canonical headers and signed headers.
canonical_headers = "host:{}\nx-amz-date:{}\n".format(host, amzdate)

# Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers lists those that you want to be included in the
# hash of the request. "Host" and "x-amz-date" are always required.
signed_headers = 'host;x-amz-date'

# Create payload hash, for get requests, the payload is an empty string ("").
payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()

# create full canonical request
canonical_request = (
    "{}\n{}\n{}\n{}\n{}\n{}"
    .format(method, canonical_uri, canonical_querystring,
            canonical_headers, signed_headers, payload_hash)
)


# CREATE THE STRING TO SIGN
# Match the algorithm to the hash algo either SHA-1 or SHA-256 (recommended)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = "{}/{}/{}/aws4_request".format(datestamp, region, service)
string_to_sign = (
    "{}\n{}\n{}\n{}"
    .format(algorithm, amzdate, credential_scope,
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())
)


# CALCULATE THE SIGNATURE
signing_key = getSignatureKey(SECRET_ACCESS_KEY, datestamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key,
                     (string_to_sign).encode('utf-8'),
                     hashlib.sha256).hexdigest()


# ADD SIGNING INFORMATION TO THE REQUEST: The signing information can be either
# in a query string value or in a header named Authorization. This code shows
# how to use a header.
authorization_header = (
    "{} Credentials={}/{}, SignedHeaders={}, Signature={}"
    .format(algorithm, ACCESS_KEY_ID,
            credential_scope, signed_headers, signature)
)

# The request can include any headers, but MUST include "host", "x-amz-date", 
# and (for this scenario) "Authorization". "host" and "x-amz-date" must
# be included in the canonical_headers and signed_headers, as noted
# earlier. Order here is not significant.
# Python note: The 'host' header is added automatically by the Python 'requests' library.
headers = {
    'x-amz-date': amzdate,
    'Authorization': authorization_header
}


# ************* SEND THE REQUEST *************
request_url = "{}?{}".format(endpoint, canonical_querystring)

print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = '.format(request_url))
r = requests.get(request_url, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: {}\n'.format(r.status_code))
print(r.text)
