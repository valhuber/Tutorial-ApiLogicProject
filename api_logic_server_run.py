#!/usr/bin/env python3
"""
  ApiLogicServer v 5.03.18

  Created on July 16, 2022 15:46:50

  $ python3 api_logic_server_run.py [Listener-IP] [port] [swagger-IP]    # starts your ApiLogicServer project

  Access the server via the Browser: http://Listener-Ip:5656

"""
import os
import sys

if len(sys.argv) > 1 and sys.argv[1].__contains__("help"):
    print("")
    print("API Logic Server - run instructions (default is localhost):")
    print("  python api_logic_server_run.py [Flask-IP] [,port [, swagger-IP]]")
    print("")
    sys.exit()

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)
os.chdir(project_dir)  # so admin app can find images, code

import logging

app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.DEBUG)  # use WARNING to reduce output
app_logger.info(f'\nAPI Logic Project Starting: {__file__}\n')

logging.getLogger('safrs').setLevel(logging.INFO)
logging.getLogger('safrs.safrs_init').setLevel(logging.INFO)

from typing import TypedDict

import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket
from api import expose_api_models, customize_api
from logic import declare_logic
from flask import Flask, redirect, send_from_directory, send_file
from safrs import ValidationError, SAFRSBase

def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    # assert path_result == env_result
    return path_result


def setup_logging(flask_app):
    setup_logic_logger = True
    if setup_logic_logger:
        logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        if flask_app.config['SQLALCHEMY_DATABASE_URI'].endswith("db.sqlite"):
            formatter = logging.Formatter('%(message).160s')  # lead tag - '%(name)s: %(message)s')
            handler.setFormatter(formatter)
            logic_logger = logging.getLogger("logic_logger")
            logic_logger.handlers = []
            logic_logger.addHandler(handler)
            app_logger.warning("\nLog width truncated for readability -- "
                               "see api_logic_server_run.py in your API Logic Project\n")
        else:
            formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        logic_logger.addHandler(handler)
        logic_logger.setLevel(logging.INFO)
        logic_logger.propagate = True

    do_engine_logging = False
    engine_logger = logging.getLogger('engine_logger')  # for internals
    if do_engine_logging:
        engine_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        engine_logger.addHandler(handler)
        engine_logger.setLevel(logging.DEBUG)

    do_safrs_logging = True
    if do_safrs_logging:
        safrs_logger = logging.getLogger('safrs.safrs_init')
        safrs_logger.setLevel(logging.CRITICAL)

    do_sqlalchemy_info = False  # True will log SQLAlchemy SQLs
    if do_sqlalchemy_info:
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class ValidationErrorExt(ValidationError):
    """
    This exception is raised when invalid input has been detected (client side input)
    Always send back the message to the client in the response
    """

    def __init__(self, message="", status_code=400, api_code=2001, detail=None, error_attributes=None):
        Exception.__init__(self)
        self.error_attributes = error_attributes
        self.status_code = status_code
        self.message = message
        self.api_code = api_code
        self.detail: TypedDict = detail


import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI

db = safrs.DB  # opens database (per config.py), setting session


def create_app(config_filename=None, swagger_host: str = None, flask_host: str = None):
    """ creates flask_app, activates API and logic """
    admin_enabled = os.name != "nt"
    def constraint_handler(message: str, constraint: object, logic_row: LogicRow):
        if constraint.error_attributes:
            detail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
        else:
            detail = {"model": logic_row.name}
        raise ValidationErrorExt(message=message, detail=detail)

    flask_app = Flask("API Logic Server", template_folder='ui/templates')  # templates to load ui/admin/admin.yaml
    flask_app.config.from_object("config.Config")
    if admin_enabled:
        flask_app.config.update(SQLALCHEMY_BINDS={'admin': 'sqlite:////tmp/4LSBE.sqlite.4'})
    # flask_app.config.update(SQLALCHEMY_BINDS = {'admin': 'sqlite:///'})
    setup_logging(flask_app)
    # ?? db = safrs.DB  # opens database per config, setting session
    Base: declarative_base = db.Model
    session: Session = db.session

    LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)

    db.init_app(flask_app)
    with flask_app.app_context():
        if admin_enabled:
            db.create_all()
            db.create_all(bind='admin')
            session.commit()

        app_logger.debug(f'\n==> Network Diagnostic - create_app exposing api on swagger_host: {swagger_host}')
        safrs_api = expose_api_models.expose_models(flask_app, swagger_host=swagger_host, PORT=port, API_PREFIX=API_PREFIX)
        customize_api.expose_services(flask_app, safrs_api, project_dir, swagger_host=swagger_host, PORT=port)  # custom services

        from database import customize_models
        app_logger.debug(f'Customizations for API and Model activated\n')

        SAFRSBase._s_auto_commit = False
        session.close()

    return flask_app, safrs_api


# address where the api will be hosted, change this if you're not running the app on localhost!
network_diagnostics = True
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# defaults from ApiLogicServer create command...
flask_host   = "localhost"  # where clients find  the API (eg, cloud server addr)
swagger_host = "localhost"  # where swagger finds the API
port = "5656"

if __name__ == "__main__":  # gunicorn-friendly host/port settings ()
    if sys.argv[1:]:
        flask_host = sys.argv[1]  # you many need to enable cors support, below
        app_logger.debug(f'==> Network Diagnostic - using specified flask_host: {sys.argv[1]}')
    else:
        app_logger.debug(f'==> Network Diagnostic - defaulting flask_host: {flask_host}')
    if is_docker() and flask_host == "localhost":
        use_docker_override = True
        if use_docker_override:
            flask_host = "0.0.0.0"  # noticeably faster (at least on Mac)
            app_logger.debug(f'==> Network Diagnostic - using docker_override for flask_host: {flask_host}')
    if sys.argv[2:]:
        port = sys.argv[2]  # you many need to enable cors support, below
        app_logger.debug(f'==> Network Diagnostic - using specified port: {sys.argv[2]}')
    if sys.argv[3:]:
        swagger_host = sys.argv[3]
        app_logger.debug(f'==> Network Diagnostic - using specified swagger_host: {sys.argv[3]}')
else:
    app_logger.debug(f'==> Network Diagnostic - WSGI server, flask_host={flask_host}, port={port}, swagger_host={swagger_host}')

API_PREFIX = "/api"
did_send_spa = False
flask_app, safrs_api = create_app(flask_host = flask_host, swagger_host = swagger_host)


@flask_app.route('/')
def index():
    app_logger.debug(f'API Logic Server - redirect /admin-app/index.html')
    return redirect('/admin-app/index.html')


@flask_app.route('/ui/admin/admin.yaml')
def admin_yaml():
    import io
    use_type = "mem"
    if use_type == "mem":
        with open("ui/admin/admin.yaml", "r") as f:
            content = f.read()
        content = content.replace("{swagger_host}", swagger_host)
        content = content.replace("{port}", port)
        content = content.replace("{api}", API_PREFIX)
        result_url = f'<http://>{swagger_host}:{port}{API_PREFIX}'
        app_logger.debug(f'loading ui/admin/admin.yaml with ~ {result_url}')
        mem = io.BytesIO(str.encode(content))
        return send_file(mem, mimetype='text/yaml')
    else:
        response = send_file("ui/admin/admin.yaml", mimetype='text/yaml')
        return response


@flask_app.route("/admin-app/<path:path>")
def send_spa(path=None):
    """ send minified safrs-react-admin app """
    global did_send_spa
    if path == "home.js":
        directory = "ui/admin"
    else:
        directory = 'ui/safrs-react-admin'
    if not did_send_spa:
        did_send_spa = True
        app_logger.debug(f'send_spa - directory = {directory}, path= {path}')
    return send_from_directory(directory, path)


@flask_app.errorhandler(ValidationError)
def handle_exception(e: ValidationError):
    res = {'code': e.status_code,
           'errorType': 'Validation Error',
           'errorMessage': e.message}
    #    if debug:
    #        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return res, 400


""" uncomment to disable cors support"""

@flask_app.after_request
def after_request(response):
    '''
    Enable CORS. Disable it if you don't need CORS or install Cors Libaray
    https://parzibyte.me/blog
    '''
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = \
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    # print(f'cors aftter_request - response: {str(response)}')
    return response


""" start the server from create_app """

if __name__ == "__main__":
    msg = f'API Logic Project Started, version 5.03.12, available at http://{swagger_host}:{port}'
    if is_docker():
        msg += f' (running from docker container at {flask_host} - may require refresh)'
    app_logger.info(msg)
    flask_app.run(host=flask_host, threaded=False, port=port)
