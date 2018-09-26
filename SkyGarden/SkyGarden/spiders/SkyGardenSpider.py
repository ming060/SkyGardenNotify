import scrapy
from scrapy_splash import SplashRequest

class SkyGardenSpider(scrapy.Spider):
	name = "events"

	def start_requests(self):
		lua_script = """
		function main(splash, args)
			assert(splash:go(args.url))
			assert(splash:wait(5))
			btn = splash:select('div.bb-months > div > div > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > td.ng-scope.available:nth-child(2) > div')
			btn:mouse_click()
			assert(splash:wait(5))
			return {
				html = splash:html(),
				png = splash:png(),
				har = splash:har(),
			}
		end
		"""

		yield SplashRequest(
			url="https://bespoke.bookingbug.com/skygarden/new_booking.html#/events",
			endpoint="execute",
			args={'wait': 5,
			'lua_source':lua_script,
			},
			callback=self.parse,
		)

	def parse(self, response):
		slot_dict = dict()
		for slot in response.xpath("//button[@class='btn btn-slot btn-primary btn-block']"):
			time = slot.xpath(".//span/div[@class='ng-binding']/text()").extract_first()
			space = slot.xpath(".//span/div[@class='event-space ng-binding']/text()").extract_first()
			slot_dict[time] = space

		self.logger.info(slot_dict)

		yield {
			"message" : response.xpath("//div[@class='col-sm-12 text-center']/h2/text()").extract_first(),
			"today" : response.xpath("//td[@class='ng-scope available selected today']/div/text()").extract(),
			"selected_date" : response.xpath("//td[@class='ng-scope available selected']/div/text()").extract(),
			"date" : response.xpath("//td[@class='ng-scope available']/div/text()").extract(),
			"month" : response.xpath("//div[@class='bb-month ng-scope slick-slide slick-current slick-active']/div/div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract(),
			"next_month" : response.xpath("//div[@class='bb-month ng-scope slick-slide slick-active']/div/div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract(),
			"slot_dict" : slot_dict,
		}
