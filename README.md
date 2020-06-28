# Web Scraping Excercise
Attempt to learn scraping using Scrapy. 

## Objectives
- Use Web scraping to scrape data off the GCP report.
- Use SQLlite to host the data automatically
- Stand a report in D3.js to start cost reporting

## Why Scrapy?
- Scrapy can scrape 960 web pages per minute. Depends on PC (8 GB RAM)
- Scrapy has 5 main components
  - Spiders- what to extract froma web page? (5 classes: Scrapy.spider, CrawlSpider, XMLFeedSpider, CSVFeedSpider, Sitemapspider)
  - Pipelines component- Data cleaning, remove duplicates and storage
  - Middleware component- Req/ Response, inject custom header and proxying
  - Engine - Coordination between components, Operational consistency
  - Scheduler-Preserving operational ordr, simple Queue

##Other Resources

