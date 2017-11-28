# amazon-search

interview prep from cracking the coding interview

## Description

Python template for Amazon Product Advertising API
(also includes example for Amazon IAM AWS API using IAM credentials)

## Features

* make request to Product Advertising API
* make signature with hash function for both API's
* interpret response

## Requirements

* Amazon Product Advertising API:
  * Association Tag
  * Unique Access Key ID
  * Secret Key

* Amazon AWS IAM API:
  * Unique Access Key ID
  * Secret Key

## Helpful Links

* Product Advertising API
  * (Sign In/ Sign Up)[https://affiliate-program.amazon.com/]
  * (Example REST API Requests)[http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html]
  * (Item Lookup)[http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemLookup.html]
  * (Item Search)[http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html]
  * (Keyword Search)[http://docs.aws.amazon.com/AWSECommerceService/latest/DG/EX_SearchingbyKeyword.html]

* AWS IAM API
  * (Sign In/ Sign Up)[https://www.amazon.com/console/home]
  * (Example Create User & Signature)[http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html]

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
