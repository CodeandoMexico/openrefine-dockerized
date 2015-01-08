#!/usr/bin/python2

from sessions.open_refine import  get_session, new_session

from flask import Flask, request, redirect
from urllib import urlencode
from urlparse import urlparse

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def root():
    resource = request.args.get("resource", "")

    encode_url = urlencode(request.args)

    ip = request.remote_addr
    logger.info("Verificando sesion activa a %s" % ip)
    active_session = get_session(ip)

    if not active_session:
        logger.info("Adquiriendo nueva sesion")
        active_session = new_session(ip)

    # Add resource parameter to existing query
    if resource != "":
        logger.info("Estableciendo query string")
        active_session = active_session + "?" + encode_url

    logger.info("Redirijiendo")
    return redirect(active_session)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
