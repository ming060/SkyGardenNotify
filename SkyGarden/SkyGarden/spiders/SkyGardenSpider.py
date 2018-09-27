import datetime
import scrapy
from scrapy_splash import SplashRequest

class SkyGardenSpider(scrapy.Spider):
	name = "events"

	def start_requests(self):
		lua_script = """
		function main(splash, args)
			assert(splash:go(args.url))
			assert(splash:wait(5))
			selector = string.format('div.bb-months > div > div > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > td.ng-scope.available:nth-child(%d) > div', args.test)
			btn = splash:select(selector)
			btn:mouse_click()
			assert(splash:wait(5))
			return {
				html = splash:html(),
				png = splash:png(),
				har = splash:har(),
			}
		end
		"""

		# yield SplashRequest(
		# 	url="https://bespoke.bookingbug.com/skygarden/new_booking.html#/events",
		# 	endpoint="execute",
		# 	args={
		# 	'test': 2,
		# 	'wait': 5,
		# 	'lua_source':lua_script,
		# 	},
		# 	callback=self.parse,
		# )

		yield SplashRequest(
			url="https://bespoke.bookingbug.com/skygarden/new_booking.html#/events",
			args={
			'wait': 5,
			},
			callback=self.parse,
		)

	def parse(self, response):
		# slot_dict = dict()
		# for slot in response.xpath("//button[@class='btn btn-slot btn-primary btn-block']"):
		# 	time = slot.xpath(".//span/div[@class='ng-binding']/text()").extract_first()
		# 	space = slot.xpath(".//span/div[@class='event-space ng-binding']/text()").extract_first()
		# 	slot_dict[time] = space
		# # self.logger.info(slot_dict)
		# slot_message = response.xpath("//span[@class='ng-binding']/text()").extract_first()
		# if slot_message == "No":
		# 	slot_count = 0
		# else:
		# 	slot_count = slot_message
		# self.logger.info(slot_count)

		time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		months = response.xpath("//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract()
		month_count = len(months)

		today = self.parse_today(response)

		current_month_selector = response.xpath("//div[@class='bb-month ng-scope slick-slide slick-current slick-active']")
		current_month = self.get_month_string(current_month_selector)
		current_month_availiable_dates = current_month_selector.xpath(".//td[@class='ng-scope available']/div/text()").extract()
		# self.logger.info("current_month_availiable_dates: %s", current_month_availiable_dates)

		next_month_selector = response.xpath("//div[@class='bb-month ng-scope slick-slide slick-active']")
		next_month = self.get_month_string(next_month_selector)
		next_month_availiable_dates = next_month_selector.xpath(".//td[@class='ng-scope available']/div/text()").extract()
		# self.logger.info("next_month_availiable_dates: %s", next_month_availiable_dates)

		total_availiable_date_count = len(current_month_availiable_dates) + len(next_month_availiable_dates)
		total_availiable_date_count += 1 # today

		yield {
			"total_availiable_date_count" : total_availiable_date_count,
			"resfresh_time" : time,
			"today" : today,
			"month_count" : month_count,
		}

	def parse_today (self, response):
		today_td = response.xpath("//td[@class='ng-scope available selected today']")
		day_of_today = today_td.xpath("./div/text()").extract_first()
		current_month = today_td.xpath("./ancestor::div[@class='bb-months']//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract_first()
		return "%s %s" % (self.process_month_string(current_month), day_of_today)

	def get_month_string(self, month_selector):
		month = month_selector.xpath(".//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract_first()
		month = self.process_month_string(month)
		return month

	def process_month_string(self, raw_string):
		processed_string = raw_string.replace(" ", "")
		stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
		processed_string = stripped(processed_string)
		return processed_string
