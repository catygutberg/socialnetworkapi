# SocialNetworkAPI

API allows to create and manage posts and likes. Also it shows users and likes statistics. User registration doesn't require authorization. To use any other endpoints user should be authorized by JWT token.

API usage documentaion can be found here: https://documenter.getpostman.com/view/18156181/UVC6jmpa 
https://www.getpostman.com/collections/1fb950ae88beca47c661


Can be deployed locally using docker/docker-compose (API and PostgreSQL containers):
```shell
docker-compose up -d
```
(in the root directory)

API listens on 8000 port on localhost.

Local PostgreSQL database located on docker volume (../socialnetworkdb). Custom DB can be specified using DATABASE_URL environment variable.


The test version of API is also deployed on Heroku at https://catysocialnetworkapi.herokuapp.com/api 
