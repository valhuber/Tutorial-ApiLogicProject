got Admin App working using Launch Configuration = ApiLogicServer

  1 - add 5656 port, start server and click port > globe
  2 - port > copy local address: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/
https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/


7/11 - I can run swagger (got this from Browser tools during admin app execution)

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'

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
  Added swagger-host as 3rd arg, updated LaunchCongig=ApiLogicServer-swagger to use it.  
  App runs, Swagger has specified URL, but hangs on Try It Now.
