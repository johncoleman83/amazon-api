# Amazon API

product advertising API & aws IAM API

## Description

Python template for Amazon Product Advertising API
(also includes example for Amazon IAM AWS API using IAM credentials)

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

* main application:

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
amazon_api.item_search_response_handler(RESPONSE)
```
* product advertising API for item Lookup
```
RESPONSE = amazon_api.item_lookup(ASIN)
amazon_api.item_lookup_response_handler(RESPONSE)
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
