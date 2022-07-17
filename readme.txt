5/17 - Launch Config: cs-main-stunning-happiness
    upgraded codespaces port mapping for 5656 -- public, http
        localAddr: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/
    merged from running branch: 5.3.18
        this branch includes api_logic_server_run.py support for dynamically comuting admin.yaml api_root
            admin.yaml contains:
                api_root:   https://{swagger_host}:{port}/{api}
            these {values} are substituted in api_logic_server_run.py, from launch-config args:
                {
                    "name": "cs-main-stunning-happiness",
                    "type": "python",
                    "request": "launch",
                    "program": "api_logic_server_run.py",
                    "redirectOutput": true,
                    "justMyCode": false,
                    "args": ["localhost", "5656", "valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev"],
                    "console": "integratedTerminal"
                },
        so users won't have to put this in launch-config AND admin.yaml 
    curl works
      curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev//api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'
    app can be hardcoded or dynamic, per admin.yaml/api_root
        works with hardcoded (see log-hardcoded.txt)
            api_root: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/api
        works with dynamic
            api_root: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/api
                Important Note:
                    the port mapping encodes the port# ====> notice no :5656 above  <====
                    so, to make the app work, we compute api_root *without*
                        ==> api_logic_server_run.py had to check CODESPACES env -- os.getenv('CODESPACES')
    swagger/get always FAILS, but now I think I know why....
        that's because this code has no way to "decline" the port; e.g., tried omitting it...
            api = SAFRSAPI(app, host=swagger_host, prefix = API_PREFIX, **kwargs)  # FAILS.. port still defaults to :5000
        I don't if this is specific to os.getenv('CODESPACES'), or more common...?