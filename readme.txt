got Admin App working using Launch Configuration = ApiLogicServer

  1 - add 5656 port, start server and click port > globe
  2 - port > copy local address: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/


7/11 - I can run swagger (got this from Browser tools during admin app execution)

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'

      later:  lose ferrer, use agent, conn alive, sec-fetch... as you can

7/11 - But, unable to run swagger using Launch Configuration = ApiLogicServer-swagger

  the 1st arg (line 24 in launch.json) is the host; set to "copy local address" from above

  fails with: OSError: [Errno 99] Cannot assign requested address
