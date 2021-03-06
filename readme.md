# Tutorial
Welcome to the Sample Database Readme - [run the Tutorial](Tutorial).

...Also available in [the docs](https://valhuber.github.io/ApiLogicServer/Tutorial/).

The standard API Logic Project readme follows...

&nbsp;

# API Logic Server


This project was created by the API Logic Server with the `ApiLogicServer create` command.  Edit / extend this readme as desired.

&nbsp;&nbsp;

# Setup and Run

### Establish your Python environment
To run your project, the system requires various runtime systems for data access, api, and logic.  These are [included with API Logic Server](https://valhuber.github.io/ApiLogicServer/Architecture-What-Is/).  The procedure for effecting this inclusion depends on your install:

* Docker - your runtime systems are part of Dev Container, which you probably activated when you [opened the project](https://valhuber.github.io/ApiLogicServer/IDE-Execute/)
* Local Installs - `pip install` your projects' virtual environment
as [described here](https://valhuber.github.io/ApiLogicServer/Project-Env/).

    * See also the `venv_setup` directory in this API Logic Project.

    * If using SqlServer, install `pyodbc`.  Not required for docker-based projects.  For local installs, see the [Quick Start](https://valhuber.github.io/ApiLogicServer/Install-pyodbc/).

### Run
Then, start the API, either by __IDE launch configurations__, or by command line: `python api_logic_server_run.py`.

* **Open the Admin App -** [http://localhost:5656/admin-app/index.html#/Home](http://localhost:5656/admin-app/index.html#/Home)


&nbsp;&nbsp;

# Project Information

| About                    | Info                               |
|:-------------------------|:-----------------------------------|
| Created                  | July 23, 2022 19:12:04                      |
| API Logic Server Version | 5.03.25           |
| Created in directory     | ../../servers/ApiLogicProject |
| API Name                 | api          |

&nbsp;&nbsp;


# Key Technologies

API Logic Server is based on the projects shown below.
Consult their documentation for important information.

### SARFS JSON:API Server

[SAFRS: Python OpenAPI & JSON:API Framework](https://github.com/thomaxxl/safrs)

SAFRS is an acronym for SqlAlchemy Flask-Restful Swagger.
The purpose of this framework is to help python developers create
a self-documenting JSON API for sqlalchemy database objects and relationships.

These objects are serialized to JSON and 
created, retrieved, updated and deleted through the JSON API.
Optionally, custom resource object methods can be exposed and invoked using JSON.

Class and method descriptions and examples can be provided
in yaml syntax in the code comments.

The description is parsed and shown in the swagger web interface.
The result is an easy-to-use
swagger/OpenAPI and JSON:API compliant API implementation.

### LogicBank

[Transaction Logic for SQLAlchemy Object Models](https://valhuber.github.io/ApiLogicServer/Logic-Why/)

Use Logic Bank to govern SQLAlchemy update transaction logic - 
multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

Logic Bank is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.
Your logic therefore applies to any SQLAlchemy-based access - JSON:Api, Admin App, etc.


### SQLAlchemy

[Object Relational Mapping for Python](https://docs.sqlalchemy.org/en/13/).

SQLAlchemy provides Python-friendly database access for Python.

It is used by JSON:Api, Logic Bank, and the Admin App.

SQLAlchemy processing is based on Python `model` classes,
created automatically by API Logic Server from your database,
and saved in the `database` directory.



### Admin App

This generated project also contains a React Admin app:
* Multi-page - including page transitions to "drill down"
* Multi-table - master / details (with tab sheets)
* Intelligent layout - favorite fields first, predictive joins, etc
* Logic Aware - updates are monitored by business logic

&nbsp;&nbsp;

# Project Structure
This project was created with the following directory structure:

| Directory | Usage                         | Key Customization File             | Typical Customization                                                                 |
|:-------------- |:------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|
| ```api``` | JSON:API                      | ```api/customize_api.py```         | Add new end points / services                                                         |
| ```database``` | SQLAlchemy Data Model Classes | ```database/customize_models.py``` | Add derived attributes, and relationships missing in the schema                       |
| ```logic``` | Transactional Logic           | ```logic/declare_logic.py```       | Declare multi-table derivations, constraints, and events such as send mail / messages |
| ```ui``` | Admin App                     | ```ui/admin/admin.yaml```          | Control field display - order, captions etc.                                          |
| ```tests``` | Behave Test Suite              | ```tests/api_logic_server_behave/features```          | Declare and implement [Behave Tests](https://valhuber.github.io/ApiLogicServer/Behave/)                                          |
&nbsp;

### Key Customization File - Typical Customization

In the table above, the _Key Customization Files_ are created as stubs, intended for you to add customizations that extend
the created API, Logic and Web App.  Since they are separate files, the project can be
[rebuilt](see api_logic_server_run.py) (e.g., synchronized with a revised schema), preserving your customizations.

Please see the ```nw``` sample for examples of typical customizations.
