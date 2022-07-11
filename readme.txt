got it working:

  1 - add 5656 port
  2 - admin url: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/api


  3 - admin url ga: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/

https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api

7/9 -- unable to run swagger, curl, or ping addr above..

  curl -X GET "https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6.githubpreview.dev/api/Category/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CCategoryName%2CDescription%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"

I got this from Browser tools during app execution.  It runs, but produces jibberish

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'

copy url parms
include=OrderDetailList
page[limit]=1

copy as curl
curl 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/Product/28?include=OrderDetailList&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers'