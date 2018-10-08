#!/usr/bin/env python
# encoding: utf-8

import datetime
import scrapy
from scrapy_splash import SplashRequest
from Scripts import LUA_SCRIPT

class SkyGardenSpider(scrapy.Spider):
	name = "events"

	def start_requests(self):
		yield SplashRequest(
			url="https://bespoke.bookingbug.com/skygarden/new_booking.html#/events",
			endpoint="execute",
			args={
				'lua_source':LUA_SCRIPT,
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
		splash_parse_time = response.data['elapsed_time']

		months = response.xpath("//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract()
		month_count = len(months)

		today = self.parse_today(response)

		current_month_selector = response.xpath("//div[@class='bb-month ng-scope slick-slide slick-current slick-active']")
		current_month = self.get_month_string(current_month_selector)
		current_month_availiable_dates = current_month_selector.xpath(".//td[@class='ng-scope available']/div/text()").extract()

		available_dates = []
		for day in current_month_availiable_dates:
			available_dates.append(self.date_string(current_month, day))

		total_availiable_date_count = len(current_month_availiable_dates)

		next_month_selector = response.xpath("//div[@class='bb-month ng-scope slick-slide slick-active']")
		if len(next_month_selector) != 0:
			next_month = self.get_month_string(next_month_selector)
			next_month_availiable_dates = next_month_selector.xpath(".//td[@class='ng-scope available']/div/text()").extract()
			for day in next_month_availiable_dates:
				available_dates.append(self.date_string(next_month, day))
			total_availiable_date_count += len(next_month_availiable_dates)

		if today is not None:
			total_availiable_date_count += 1

		yield {
			"total_availiable_date_count" : total_availiable_date_count,
			"resfresh_time" : time,
			"splash_parse_time" : splash_parse_time,
			"today" : today,
			"month_count" : month_count,
			"available_dates" : available_dates,
		}

	def parse_today (self, response):
		today_td = response.xpath("//td[@class='ng-scope available selected today']")
		if today_td is None:
			return None

		day_of_today = today_td.xpath("./div/text()").extract_first()
		current_month = today_td.xpath("./ancestor::div[@class='bb-months']//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract_first()
		return self.date_string(self.process_month_string(current_month), day_of_today)

	def get_month_string(self, month_selector):
		month = month_selector.xpath(".//div[@class='month-pic-heading text-center col-xs-4 visible-xs']/b/text()").extract_first()
		month = self.process_month_string(month)
		return month

	def process_month_string(self, raw_string):
		processed_string = raw_string.replace(" ", "")
		stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
		processed_string = stripped(processed_string)
		return processed_string

	def date_string(self, month, day):
		return "%s %s" % (month, day)