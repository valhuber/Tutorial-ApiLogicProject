got it working:

  1 - add 5656 port
  2 - admin url: https://valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev/api


  3 - admin url ga: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/

https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api

7/9 -- unable to run swagger, curl, or ping addr above..

  curl -X GET "https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6.githubpreview.dev/api/Category/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CCategoryName%2CDescription%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"
