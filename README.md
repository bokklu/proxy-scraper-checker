# proxy-scraper-checker
A simple proxy scraper that scrapes and filters thousands of public proxies from the web

This 'proxy-scraper-checker' is basically a scheduler that will execute periodic jobs to check for public proxies.
Every job will scrape and ping/check proxies asynchronously and collect additional information on the proxy.

## Features:
Supports the following protocols:
- HTTP
- HTTPS
- HTTP/S
- SOCKS4
- SOCKS5
- SOCKS4/5

Every proxy will have the following statistics generated by our checker:
- address
- country
- proxy access type
- proxy type
- proxy speed
- proxy uptime
- proxy location information

The Proxy Location information entails the following properties:
- internet service provider id
- internet service provider name
- region
- timezone
- latitude/longtitude co-ordinates
- postal code
- location accuracy radius

The proxies are then saved to an external PostgreSQL database.

## Environment:
Environmental components (PostgreSQL) are Docker based. The docker-compose.yml file found in the root directory of the project makes it easier for local development as it runs the dependent components in containers.

To build and run the python-scraper-checker locally (order is important):
- docker-compose up db
- docker-compose up proxy-api
- docker-compose up proxy-scraper-checker

To run the python-scraper-checker directly from python:
- python main.py

### Ports used:
- PostgeSQL: **5432**

### Environment Variables used:
In order to make it easier to manage and keep all environment variables together, create a **.env** file in the root project directory and populate it with the environment variables listed below. This file should be left out when committing, as it might contain sensitive information.

#### Proxy-Scraper-Checker Environment Variables:
- PSC_SETTINGS  [Development or Production]
- PSC_DBPASSWORD [Database password]

##### Component Dependencies:
#### PostgreSQL Container Environment Variables:
- POSTGRES_DB [Database name]
- POSTGRES_USER [Database user]
- POSTGRES_PASSWORD [Database password]
- POSTGRES_ENVIRONMENT [Development or Production]


## Requirements:
- Python **3.7** or higher
- asyncio
- aiohttp
- aiohttp-socks
- asyncpg
- schedule
- aenum
- recordclass
- geoip2
- uvloop
- dependency-injector
