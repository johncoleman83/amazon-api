# Amazon API

product advertising API & aws IAM API. Demo: https://cecinestpasun.site/amazon/

## Description

Python template for Amazon Product Advertising API. I built this for
educational purposes only to learn about Amazon's API. The intended use of the
Product Advertising API is to direct traffic to amazon.com. Amazon offers
payment in exchange for this advertising based on how much traffic your website
generates. The API response includes various links with the user's Association
Tag and hashed key information in the query string. This is used to verify
if the data from your API has generated traffic. See the Demo for real examples.

(the source code also includes an unused example for Amazon IAM AWS API using
Amazon AWS IAM credentials)

## Disclaimer

* This is a DEMO Application, for educational use
* Not for commercial use
* This is not an official Amazon product nor endorsed by Amazon
* The author is in no way affiliated with Amazon
* The author makes no money from this application
  * unless, however, the users click the demo links/advertisements, which then
  leads to an Amazon purchase.

## Environment

* __OS:__ Linux Ubuntu 14.04 LTS
* __languages:__ Python 3.6.3
* __API__: Amazon Product Advertising & AWS IAM

## Features

* make request to Product Advertising API
* make signature with hash function for both API's
* interpret response

## Requirements

* Python:

```
$ pip3 install -r requirements.txt
```

#### Required Amazon Access Keys

* Amazon Product Advertising API:
  * Association Tag
  * Unique Access Key ID
  * Secret Key

* Amazon AWS IAM API:
  * Unique Access Key ID
  * Secret Key

## Usage

* main flask application:

```
$ ./app.py
```

#### use amazon_api python module methods

* product advertiseing API for item Search
```
import amazon_api
RESPONSE = amazon_api.item_search(
    [SEARCH_TERM, SEARCH_TERM], BRAND, SEARCH_INDEX
)
AMAZON_OBJECTS = amazon_api.item_search_response_handler(RESPONSE)
```
* product advertising API for item Lookup
```
RESPONSE = amazon_api.item_lookup(ASIN)
AMAZON_OBJECTS = amazon_api.item_lookup_response_handler(RESPONSE)
```

## Helpful Links

* Product Advertising API
  * [Sign In/ Sign Up](https://affiliate-program.amazon.com/)
  * [Example REST API Requests](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html)
  * [Item Lookup](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemLookup.html)
  * [Item Search](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html)
  * [Keyword Search](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/EX_SearchingbyKeyword.html)

* AWS IAM API
  * [Sign In/ Sign Up](https://www.amazon.com/console/home)
  * [Example Create User & Signature](http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html)

## Examples:

* [Amazon Product Advertising API Signature Creation](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html)

```
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
```

## Project Concept from Cracking the Code Interview Prep

* Take Amazon ID in as input
* Load Amazon page from internet
* Possibly in a multithreaded way
* Extract info with regex
* Confirm something with user
* Save images
* Run tests. Handle errors

## License
MIT License
