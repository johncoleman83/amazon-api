#!/usr/bin/env python3
"""
This file contains AWS IAM Access Key and Secret Key
"""
import amazon_api
import sys

if __name__ == "__main__":
    """
    MAIN APP
    """
    response = amazon_api.amazon_prod_add_api_search(
        ["mirrorless_camera"], None, None
    )
    if response is None:
        print("There was an error with this request", file=sys.stderr)
        sys.exit()
    amazon_api.search_response_handler(response)
