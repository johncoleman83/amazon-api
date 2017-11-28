#!/usr/bin/python3
"""
imports Flask instance for gunicorn configurations
gunicorn --bind 127.0.0.1:8003 wsgi.wsgi_amazon.amazon.app
"""

amazon = __import__('app', globals(), locals(), ['*'])

if __name__ == "__main__":
    """runs the main flask app"""
    amazon.app.run()
