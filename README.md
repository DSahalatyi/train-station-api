# Train station API
API service for ordering train tickets written on DRF

## Installing using GitHub
```shell
# clone the project and install the dependencies
git clone https://github.com/DSahalatyi/train-station-api
cd train-station-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# set environmental variables
set DJANGO_SECRET_KEY=<your secret key>
set POSTGRES_PASSWORD=<your db password>
set POSTGRES_USER=<your db user>
set POSTGRES_DB=<your db>
set POSTGRES_HOST=<your db host>
set POSTGRES_PORT=<your db port>
```
or configure `.env` file according to `.env.example`

## Run with docker
- Configure .env file according to .env.example
```shell
docker-compose build
docker-compose up
```

## Getting access
- create a user via /api/v1/user/register/
- get access token via /api/v1/user/token/

## Features
- JWT authentication
- Admin panel /admin/
- Documentation at /api/v1/doc/swagger/
- Managing orders and train station
- Creating stations, routes, trains and trips
- Filtering trips by `from`, `to`, `date`

## Optional
Set up Redis cache
- Configure the .env file or
```shell
set REDIS_CACHE=1
set REDIS_HOST=<your redis host>
set REDIS_PASSWORD=<your redis password>
```