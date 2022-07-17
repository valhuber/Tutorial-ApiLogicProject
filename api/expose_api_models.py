from safrs import SAFRSAPI
import safrs
import importlib
import pathlib
import logging as logging

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

app_logger = logging.getLogger('api_logic_server_app')
app_logger.info("api/expose_api_models.py - endpoint for each table")


def expose_models(app, swagger_host="localhost", PORT=5656, API_PREFIX="/api", **kwargs):
    """ create SAFRSAPI, exposing each model (note: end point names are table names) """
    import os
    app_logger.debug(f"api/expose_api_models -- swagger_host = {swagger_host}, port = {PORT}")
    if os.getenv('CODESPACES'):  # port is implicit and gets mapped
        api = SAFRSAPI(app, host=swagger_host, prefix = API_PREFIX, **kwargs)  # FAILS, defaults to 5000
    else:
        api = SAFRSAPI(app, host=swagger_host, port=PORT, prefix = API_PREFIX, **kwargs)
    safrs_log_level = safrs.log.getEffectiveLevel()
    if True or app_logger.getEffectiveLevel() >= logging.INFO:
        safrs.log.setLevel(logging.WARN)  # warn is 20, info 30
    api.expose_object(database.models.Category)
    api.expose_object(database.models.Customer)
    api.expose_object(database.models.CustomerDemographic)
    api.expose_object(database.models.Department)
    api.expose_object(database.models.Employee)
    api.expose_object(database.models.Union)
    api.expose_object(database.models.EmployeeAudit)
    api.expose_object(database.models.EmployeeTerritory)
    api.expose_object(database.models.Territory)
    api.expose_object(database.models.Location)
    api.expose_object(database.models.Order)
    api.expose_object(database.models.OrderDetail)
    api.expose_object(database.models.Product)
    api.expose_object(database.models.Region)
    api.expose_object(database.models.SampleDBVersion)
    api.expose_object(database.models.Shipper)
    api.expose_object(database.models.Supplier)
    safrs.log.setLevel(safrs_log_level)
    return api
