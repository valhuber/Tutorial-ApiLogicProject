got Admin App working using Launch Configuration = ApiLogicServer

  1 - add 5656 port, start server and click port > globe
  2 - port > copy local address: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/
https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/
  http://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656/api



7/11 - I can run swagger (got this from Browser tools during admin app execution)

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' 


      later:  lose ferrer, use agent, conn alive, sec-fetch... as you can

7/11 - But, unable to run swagger using Launch Configuration = ApiLogicServer-swagger

  the 1st arg (line 24 in launch.json) is the host; set to "copy local address" from above

  fails with: OSError: [Errno 99] Cannot assign requested address 
    and, once fails, must restart server

7/13 - Following Thomas' advice for flask_host vs. swagger_host...

  TL;DR  -- pythonanywhere
      2022-07-14 01:41:52 ==> Network Diagnostic - not main, will start flask with [flask] host: apilogicserver.pythonanywhere.com
      2022-07-14 01:41:52 ==> Network Diagnostic - swagger_host: apilogicserver.pythonanywhere.com 

  TL;DR -- local docker
      ==> Network Diagnostic - using docker flask_host: 0.0.0.0
      ==> Network Diagnostic - create_app exposes api on [swagger] host localhost
          api/expose_api_models -- host = localhost, port = 5656
      API Logic Project Started, version 5.03.12, available at http://localhost:5656 (running from docker container at 0.0.0.0 - may require refresh)

  TL;DR -- Codespaces {ApiLogicServer}
      ==> Network Diagnostic - create_app exposes api on [swagger] host 127.0.0.1
      API Logic Project Started, version 5.02.17, available at http://localhost:5656 on docker container at flask_host: 127.0.0.1

  TL;DR -- Codespaces {ApiLogicServer-swagger}
      ==> Network Diagnostic - create_app exposes api on [swagger] host valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
      API Logic Project Started, version 5.02.17, available at http://localhost:5656 on docker container at flask_host: valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
        Fails to start server with "Cannot assign requested address"

  TL;DR -- Codespaces {ApiLogicServer-swagger with flask_host override}
      ==> Network Diagnostic - create_app exposes api on [swagger] host valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
      API Logic Project Started, version 5.02.17, available at http://localhost:5656 on docker container at flask_host: 127.0.0.1

      this runs better - app runs, swagger has right url, but hangs... public port?? No, still fails using "public"

7/14
  Added swagger-host as 3rd arg, updated LaunchConfig=ApiLogicServer-swagger to use it.  
  App runs, Swagger has specified URL, but hangs on Try It Now.  
    Public does not help.  http did not seem to help
  Curl now fails with 302
    <html>
    <head><title>302 Found</title></head>
      <body>
        <center><h1>302 Found</h1></center>
        <hr><center>nginx/1.17.7</center>
      </body>
    </html>
  Networking is flaky - I often need to restart server, or delete/re-add port 
    1 - log info
      127.0.0.1 - - [15/Jul/2022 02:12:49] code 400, message Bad request version ("´\x80\x8b-ø«®\x00>\x13\x02\x13\x03\x13\x01À,À0\x00\x9fÌ©Ì¨ÌªÀ+À/\x00\x9eÀ$À(\x00kÀ#À'\x00gÀ")
      127.0.0.1 - - [15/Jul/2022 02:12:49] "2.ÑeÈJ%ø)eg¯õ89ÖDÓab¬û¸osuì îúâýz4ÁYJI´ï\Ò@*IBñÃj´-ø«®>À,À0©Ì¨ÌªÀ+À/$À(kÀ#À'gÀ" HTTPStatus.BAD_REQUEST -
    2 - Bad Gateway on starting the globe
  Options I tried
    1 - In launch config, change flask-port to localhost
    2 - And, disable api_logic_server_run.py -- use_docker_override = False


7/15 - cURL now running

  Changed Port Visibility to public, then it ran

7/16 - explore 5.3.18 using launch: upgraded-enigma

  runs, but only hard coded
    fails: 
      api_root: >-https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656/api
    works (not-mem):
                  https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api
    cURL works:
      curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'

7/17 - launch: upgraded-enigma    port: public, http
  cURL still works
  works with nonMem

    API Logic Project Starting: api_logic_server_run.py

    api/expose_api_models.py - endpoint for each table
    database/db.py - got session: <sqlalchemy.orm.scoping.scoped_session object at 0x7fc01d39d9a0>
    logic/__init__ begin
    logic/declare_logic.py - importing declare_logic
    logic/__init__ end

    ==> Network Diagnostic - using specified flask_host: localhost
    ==> Network Diagnostic - using docker_override for flask_host: 0.0.0.0
    ==> Network Diagnostic - using specified port: 5656
    ==> Network Diagnostic - using specified swagger_host: valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
    config.py - db_url: sqlite:////workspaces/Tutorial-ApiLogicProject/database/db.sqlite
    config.py - SQLALCHEMY_DATABASE_URI: sqlite:////workspaces/Tutorial-ApiLogicProject/database/db.sqlite

    Log width truncated for readability -- see api_logic_server_run.py in your API Logic Project



    logic/logic_bank.py: declare_logic complete
    Logic Bank 01.07.01 - 22 rules loaded

    ==> Network Diagnostic - create_app exposing api on swagger_host: valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
    api/expose_api_models -- swagger_host = valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev, port = 5656
    /usr/local/lib/python3.9/site-packages/safrs/base.py:929: SAWarning: Dialect sqlite+pysqlite does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point - rounding errors and other issues may occur. Please consider storing Decimal numbers as strings or integers on this platform for lossless storage.
      sample = cls.query.first()

    *** Customizable API Logic Project created -- open it with your IDE at /workspaces/Tutorial-ApiLogicProject
    *** Server now running -- explore sample data and API at swagger_host: http://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656/

    api/expose_service.py - Exposing custom services
    database/customize_models.py - models.Employee.Manager(manages), Employee.ProperSalary

    Customizations for API and Model activated

    API Logic Project Started, version 5.03.12, available at http://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656 (running from docker container at 0.0.0.0 - may require refresh)
    * Serving Flask app "API Logic Server" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Running on all addresses.
      WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://172.16.5.4:5656/ (Press CTRL+C to quit)

  fails with Mem
    API Logic Project Starting: api_logic_server_run.py

    api/expose_api_models.py - endpoint for each table
    database/db.py - got session: <sqlalchemy.orm.scoping.scoped_session object at 0x7f4821c5e9a0>
    logic/__init__ begin
    logic/declare_logic.py - importing declare_logic
    logic/__init__ end

    ==> Network Diagnostic - using specified flask_host: localhost
    ==> Network Diagnostic - using docker_override for flask_host: 0.0.0.0
    ==> Network Diagnostic - using specified port: 5656
    ==> Network Diagnostic - using specified swagger_host: valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
    config.py - db_url: sqlite:////workspaces/Tutorial-ApiLogicProject/database/db.sqlite
    config.py - SQLALCHEMY_DATABASE_URI: sqlite:////workspaces/Tutorial-ApiLogicProject/database/db.sqlite

    Log width truncated for readability -- see api_logic_server_run.py in your API Logic Project



    logic/logic_bank.py: declare_logic complete
    Logic Bank 01.07.01 - 22 rules loaded

    ==> Network Diagnostic - create_app exposing api on swagger_host: valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev
    api/expose_api_models -- swagger_host = valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev, port = 5656
    /usr/local/lib/python3.9/site-packages/safrs/base.py:929: SAWarning: Dialect sqlite+pysqlite does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point - rounding errors and other issues may occur. Please consider storing Decimal numbers as strings or integers on this platform for lossless storage.
      sample = cls.query.first()

    *** Customizable API Logic Project created -- open it with your IDE at /workspaces/Tutorial-ApiLogicProject
    *** Server now running -- explore sample data and API at swagger_host: http://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656/

    api/expose_service.py - Exposing custom services
    database/customize_models.py - models.Employee.Manager(manages), Employee.ProperSalary

    Customizations for API and Model activated

    API Logic Project Started, version 5.03.12, available at http://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev:5656 (running from docker container at 0.0.0.0 - may require refresh)
    * Serving Flask app "API Logic Server" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Running on all addresses.
      WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://172.16.5.4:5656/ (Press CTRL+C to quit)

