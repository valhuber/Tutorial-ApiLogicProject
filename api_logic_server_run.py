#!/usr/bin/env python3

"""  hello Max
==============================================================================

    This file starts the API Logic Server (v 5.03.25, July 23, 2022 19:12:04):
        $ python3 api_logic_server_run.py [--help  # host, port arguments]

    Then, access the Admin App and API via the Browser, eg:  
        http://localhost:5656

    You typically do not customize this file,
        except to override Creation Defaults and Logging, below.

    See Main Code (at end).
        Use log messages to understand API and Logic activation.

==============================================================================
"""

import os, logging, sys


def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    # assert path_result == env_result
    return path_result


# =======================================
#    Creation Defaults
#
#        Override as desired
#         Or specify in CLI arguments
# ======================================= 

# defaults from ApiLogicServer create command...
API_PREFIX = "/api"
flask_host   = "localhost"  # where clients find  the API (eg, cloud server addr)
swagger_host = flask_host  # where swagger finds the API
if is_docker() and flask_host == "localhost":
    flask_host = "0.0.0.0"  # noticeably faster (at least on Mac)
port = "5656"
swagger_port = port  # for codespaces - see values in launch config
http_type = "http"

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)
os.chdir(project_dir)  # so admin app can find images, code

# ==================================
#       LOGGING SETUP
# ================================== 

app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.INFO)  # log levels: critical < error < warning(20) < info(30) < debug
app_logger.info(f'\nAPI Logic Project Starting: {__file__}')

logging.getLogger('safrs').setLevel(logging.INFO)
logging.getLogger('safrs.safrs_init').setLevel(logging.INFO)

from typing import TypedDict
import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket
import warnings
from api import expose_api_models, customize_api
from logic import declare_logic
from flask import Flask, redirect, send_from_directory, send_file
from safrs import ValidationError, SAFRSBase
from typing import TypedDict
import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket
import warnings
from api import expose_api_models, customize_api
from logic import declare_logic
from flask import Flask, redirect, send_from_directory, send_file
from safrs import ValidationError, SAFRSBase
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI


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


db = safrs.DB

def flask_events(flask_app):
    """ events for serving admin.yaml, minified safrs-admin
    """
    @flask_app.route('/')
    def index():
        app_logger.debug(f'API Logic Server - redirect /admin-app/index.html')
        return redirect('/admin-app/index.html')


    @flask_app.route('/ui/admin/admin.yaml')
    def admin_yaml():
        """
        returns response of admin.yaml
        and text-substitutes to get url args from startup args (vs. specify them twice)
            api_root: {http_type}://{swagger_host}:{swagger_port} (from ui_admin_creator)
        """
        import io
        use_type = "mem"
        if use_type == "mem":
            with open("ui/admin/admin.yaml", "r") as f:
                content = f.read()
            content = content.replace("{http_type}", http_type)
            content = content.replace("{swagger_host}", swagger_host)
            content = content.replace("{port}", swagger_port)  # note - codespaces requires 443 here (typically via args)
            content = content.replace("{api}", API_PREFIX[1:])
            app_logger.debug(f'loading ui/admin/admin.yaml')
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


    @flask_app.after_request
    def after_request(response):
        '''
        Enable CORS. Disable it if you don't need CORS or install Cors Library
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


def get_args():
    """
    returns tuple: (flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run)
    """

    global flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run

    network_diagnostics = True
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    verbose = False
    create_and_run = False

    def make_wide(formatter, w=120, h=36):
        """ Return a wider HelpFormatter, if possible."""
        try:
            # https://stackoverflow.com/a/5464440
            # beware: "Only the name of this class is considered a public API."
            kwargs = {'width': w, 'max_help_position': h}
            formatter(None, **kwargs)
            return lambda prog: formatter(prog, **kwargs)
        except TypeError:
            warnings.warn("argparse help formatter failed, falling back.")
            return formatter

    if __name__ == "__main__":  # gunicorn-friendly host/port settings ()

        # thanks to https://www.geeksforgeeks.org/command-line-arguments-in-python/#argparse
        import argparse
        # Initialize parser
        if len(sys.argv) == 1:
            app_logger.debug("No host/port arguments - using creation defaults")
        else:
            msg = "API Logic Project"
            parser = argparse.ArgumentParser(
                formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter))
            parser.add_argument("--port",
                                help = f'port (Flask)', default = port)
            parser.add_argument("--flask_host", 
                                help = f'ip to which flask will be bound', 
                                default = flask_host)
            parser.add_argument("--swagger_host", 
                                help = f'ip clients use to access API',
                                default = swagger_host)
            parser.add_argument("--swagger_port", 
                                help = f'swagger port (eg, 443 for codespaces)',
                                default = port)
            parser.add_argument("--http_type", 
                                help = f'http or https',
                                default = "http")
            parser.add_argument("--verbose", 
                                help = f'for more logging',
                                action=argparse.BooleanOptionalAction,
                                default = False)
            parser.add_argument("--create_and_run", 
                                help = f'system use - log how to open project',
                                action=argparse.BooleanOptionalAction,
                                default = False)
            
            parser.add_argument("flask_host_p", nargs='?', default = flask_host)
            parser.add_argument("port_p", nargs='?', default = port)
            parser.add_argument("swagger_host_p", nargs='?', default = swagger_host)
            
            args = parser.parse_args()

            """
                accepting both positional (compatibility) and keyword args... 
                cases that matter:
                    no args
                    kw only:        argv[1] starts with -
                    pos only
                positional values always override keyword, so decide which parsed values to use...
            """
            if sys.argv[1].startswith("-"):     # keyword arguments
                port = args.port
                flask_host = args.flask_host
                swagger_host = args.swagger_host
                swagger_port = args.swagger_port
                http_type = args.http_type
                verbose = args.verbose
                create_and_run = args.create_and_run
            else:                               # positional arguments (compatibility)
                port = args.port_p
                flask_host = args.flask_host_p
                swagger_host = args.swagger_host_p

    return flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run

def create_app(swagger_host: str = None, swagger_port: str = None):
    """ creates flask_app, activates API and logic """
    # https://stackoverflow.com/questions/34674029/sqlalchemy-query-raises-unnecessary-warning-about-sqlite-and-decimal-how-to-spe

    from sqlalchemy import exc as sa_exc

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)  # alert - disable for safety msgs
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

        setup_logging(flask_app)
        Base: declarative_base = db.Model
        session: Session = db.session

        safrs_log_level = safrs.log.getEffectiveLevel()
        db_logger = logging.getLogger('sqlalchemy')
        db_log_level = db_logger.getEffectiveLevel()
        if True or app_logger.getEffectiveLevel() >= logging.INFO:
            safrs.log.setLevel(logging.WARN)  # warn is 20, info 30
            db_logger.setLevel(logging.WARN)

        LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)  # opens db
        import database.db
        app_logger.info("Declare   Logic complete - logic/declare_logic.py (rules + code)"
            + f' -- {len(database.models.metadata.tables)} tables loaded')

        db.init_app(flask_app)
        with flask_app.app_context():
            if admin_enabled:
                db.create_all()
                db.create_all(bind='admin')
                session.commit()

            app_logger.info(f"\nDeclare   API - api/expose_api_models, endpoint for each table on {swagger_host}:{swagger_port}")
            safrs_api = expose_api_models.expose_models(flask_app, swagger_host=swagger_host, PORT=swagger_port, API_PREFIX=API_PREFIX)
            app_logger.info("Customize API - api/expose_service.py, exposing custom services")
            customize_api.expose_services(flask_app, safrs_api, project_dir, swagger_host=swagger_host, PORT=port)  # custom services

            app_logger.info("\nCustomize Data Model - database/customize_models.py")
            from database import customize_models

            SAFRSBase._s_auto_commit = False
            session.close()
        
        safrs.log.setLevel(safrs_log_level)
        db_logger.setLevel(db_log_level)
        return flask_app, safrs_api


did_send_spa = False

# ==================================
#        MAIN CODE
# ================================== 

(flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run) = get_args()

if verbose:
    app_logger.setLevel(logging.DEBUG)

flask_app, safrs_api = create_app(swagger_host = swagger_host, swagger_port = swagger_port)
flask_events(flask_app)

if __name__ == "__main__":
    msg = f'API Logic Project Loaded (not WSGI), version 5.03.25, configured for http://{swagger_host}:{port}\n'
    if is_docker():
        msg += f' (running from docker container at {flask_host} - may require refresh)'
    app_logger.info(f'\n{msg}')

    if create_and_run:
        app_logger.info(f'==> Customizable API Logic Project created and running -- '
                    f'open it with your IDE at {project_dir}\n')

    if os.getenv('CODESPACES'):
        app_logger.info(f'Server starting on Codespaces -- '  # FIXME (2)
                f'explore sample data and API on swagger_host: {http_type}://{swagger_host}/\n')
    else:
        app_logger.info(f'Server starting -- '  # FIXME (2)
                f'explore sample data and API on swagger_host: {http_type}://{swagger_host}:{port}/\n')

    flask_app.run(host=flask_host, threaded=False, port=port)
else:
    msg = f'API Logic Project Loaded (WSGI), version 5.03.25, configured for {http_type}://{swagger_host}:{port}\n'
    if is_docker():
        msg += f' (running from docker container at {flask_host} - may require refresh)'
    app_logger.info(f'\n{msg}')
