#!/usr/bin/env python3
"""
This file contains AWS IAM Access Key and Secret Key
"""
import amazon_api
from flask import Flask, Markup, render_template, request, url_for
import json
import requests
import sys
from uuid import uuid4


# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


def clean_inputs(word):
    """
    cleans inputs in case of blanks or all spaces
    """
    invalid_tems = [None, ' ', '', '\t', '\n']
    if word in invalid_tems:
        return None
    else:
        return word


def format_amazon_objects(amazon_objects):
    """
    adds proper formatting for html rendering of Amazon Objects
    """
    if "ERROR" in amazon_objects[0]:
        return
    for amazon_object in amazon_objects:
        page_url = Markup(
            '<a href="{}" target="_blank">Amazon Page URL</a>'
            .format(amazon_object.get("Detail Page URL")))
        amazon_object["Detail Page URL"] = page_url
        technical_url = Markup(
            '<a href="{}" target="_blank">Amazon Page URL</a>'
            .format(amazon_object.get("Technical Details")))
        amazon_object["Technical Details"] = technical_url
        image = Markup('<img src="{}" style="width: 100%;">'
                       .format(amazon_object.get("Large Image")))
        amazon_object["Large Image"] = image


@app.route('/', methods=['GET', 'POST'])
def main_index():
    """
    handles request to main index, currently a login page
    """
    cache_id = uuid4()
    if request.method == 'GET':
        return render_template('index.html', cache_id=cache_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Search Items':
            keywords = request.form.get('keywords', None)
            keywords = clean_inputs(keywords)
            if keywords is not None:
                keywords = keywords.split(', ')
            brand = request.form.get('brand', None)
            brand = clean_inputs(brand)
            search_index = request.form.get('search-index', None)
            search_index = clean_inputs(search_index)
            if brand and not search_index or (not brand and not keywords):
                return render_template('index.html', cache_id=cache_id)
            response = amazon_api.item_search(
                keywords, brand, search_index
            )
            if response is None:
                error = {"ERROR": "Unknown Error"}
                amazon_objects = [error]
            else:
                amazon_objects = amazon_api.item_search_response_handler(
                    response
                )
        elif action == 'Lookup Item':
            asin = request.form.get('asin-num', None)
            asin = clean_inputs(asin)
            if asin is None:
                return render_template('index.html', cache_id=cache_id)
            response = amazon_api.item_lookup(asin)
            amazon_objects = amazon_api.item_lookup_response_handler(response)
        else:
            error = {"ERROR": "Unknown Error"}
            amazon_objects = [error]
        format_amazon_objects(amazon_objects)
        return render_template(
            'results.html', cache_id=cache_id, amazon_objects=amazon_objects
        )


@app.errorhandler(404)
def page_not_found(error):
    """
    404 Error Handler
    """
    cache_id = uuid4()
    return render_template('404.html', cache_id=cache_id), 404


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
