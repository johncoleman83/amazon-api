#!/usr/bin/env python3
"""
AMAZON IAM API from AWS
NOT PRODUCT ADVERTISING API
This file contains AWS GET request templates from
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
and
http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
AWS Version 4 signing example - EC2 API (DescribeRegions)
"""
from authentication import ACCESS_KEY_ID, SECRET_ACCESS_KEY
import sys, os, base64, datetime, hashlib, hmac, urllib.parse
import requests

if all([ACCESS_KEY_ID, SECRET_ACCESS_KEY]) is False:
    print("Please provide ACCESS_KEY and SECRET_KEY", file=sys.stderr)
    sys.exit()


method = 'GET'
service = 'iam'
host = 'iam.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://iam.amazonaws.com'

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ') # Format date as YYYYMMDD'T'HHMMSS'Z'
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope


# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 2: Create canonical URI--the part of the URI from domain to query
# string (use '/' if no path)
canonical_uri = '/'

# Step 3: Create the canonical headers and signed headers. Header names
# must be trimmed and lowercase, and sorted in code point order from
# low to high. Note trailing \n in canonical_headers.
# signed_headers is the list of headers that are being included
# as part of the signing process. For requests that use query strings,
# only "host" is included in the signed headers.
canonical_headers = "host:{}\n".format(host)
signed_headers = 'host'

# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = "{}/{}/{}/aws4_request".format(datestamp, region, service)


# Step 4: Create the canonical query string. In this example, request
# parameters are in the query string. Query string values must
# be URL-encoded (space=%20). The parameters must be sorted by name.
canonical_querystring = 'Action=CreateUser&UserName=NewUser&Version=2010-05-08'
canonical_querystring += '&X-Amz-Algorithm=AWS4-HMAC-SHA256'
canonical_querystring += '&X-Amz-Credential=' + urllib.parse.quote_plus("{}/{}".format(ACCESS_KEY_ID, credential_scope))
canonical_querystring += '&X-Amz-Date=' + amzdate
canonical_querystring += '&X-Amz-Expires=30'
canonical_querystring += '&X-Amz-SignedHeaders=' + signed_headers

# Step 5: Create payload hash. For GET requests, the payload is an
# empty string ("").
# ADDED .encode('utf-8')
payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()
# create full canonical request
canonical_request = (
    "{}\n{}\n{}\n{}\n{}\n{}"
    .format(method, canonical_uri, canonical_querystring,
            canonical_headers, signed_headers, payload_hash)
)


# ************* TASK 2: CREATE THE STRING TO SIGN*************
# added .encode('utf-8') here, might not be accurate
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


# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# The auth information can be either in a query string
# value or in a header named Authorization. This code shows how to put
# everything into a query string.
canonical_querystring += '&X-Amz-Signature=' + signature


# ************* SEND THE REQUEST *************
request_url = "{}?{}".format(endpoint, canonical_querystring)

print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = '.format(request_url))
#r = requests.get(request_url, headers=headers)
r = requests.get(request_url)
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: {}\n'.format(r.status_code))
print(r.text)
