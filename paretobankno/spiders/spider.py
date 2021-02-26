import scrapy

from scrapy.loader import ItemLoader
from ..items import ParetobanknoItem
from itemloaders.processors import TakeFirst


class ParetobanknoSpider(scrapy.Spider):
	name = 'paretobankno'
	start_urls = ['https://blogg.paretobank.no/']

	def parse(self, response):
		post_links = response.xpath('//h1/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next-posts-link"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="section post-header"]/h1/a/span/text()').get()
		description = response.xpath('//div[@class="post-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@id="hubspot-author_data"]/text()[normalize-space()]').get()

		item = ItemLoader(item=ParetobanknoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
