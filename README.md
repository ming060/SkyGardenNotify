# SkyGardenNotify

A Web crawler to fetch avaliable spaces from [Sky Garden](https://bespoke.bookingbug.com/skygarden/new_booking.html#/events) booking site.

## How to run?
### Prerequisites
1. [Scrapy](https://scrapy.org/)
2. [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)

Run splash in Docker
```
$ docker run -p 8050:8050 scrapinghub/splash
```
Run Scrapy Spider
```
$ cd SkyGarden
$ scrapy crawl events
```
