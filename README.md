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
Environmental components (PostgreSQL) are Docker based. The docker-compose.yml file found in the root directory of the project should be used for local development.

### Development - Building the artifact
To build and run the python-scraper-checker locally:
- docker-compose up --build
## Requirements:
- Python **3.7** or higher
- asyncio
- aiohttp
- aiohttp-socks
- asyncpg
- schedule
- uvloop
