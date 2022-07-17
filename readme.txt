5/17 - Launch Config: cs-main-stunning-happiness  port: public, http
    merged from running branch: 5.3.18
    upgraded launch config for port local: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/
    curl works
      curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev//api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'
    app can be hardcoded or dynamic, per admin.yaml/api_root
        works with hardcoded (see log-hardcoded.txt)
            api_root: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/api
        FAILS with dynamic
            api_root: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev:5656/api
    swagger/get always FAILS