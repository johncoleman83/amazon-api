#!/usr/bin/env python3
"""
This file contains AWS IAM Access Key and Secret Key
"""
import amazon_api
import sys


def app():
    """
    main amazon search app
    """
    response = amazon_api.item_search(
        ["mirrorless_camera"], None, None
    )
    if response is None:
        print("There was an error with this request", file=sys.stderr)
        sys.exit()
    amazon_api.item_search_response_handler(response)


if __name__ == "__main__":
    """
    MAIN APP
    """
    app()
