import scrapy


class MangaExtractorSpider(scrapy.Spider):
    name = 'manga_extractor'
    allowed_domains = ['www.mangareader.net']
    start_urls = ['https://www.mangareader.net/alphabetical']

    def parse(self, response):
        titles = response.xpath("//div[@class='d40']/div/ul/li")
        
        for mangas in titles:
            title = mangas.xpath(".//a/text()").get()
            manga_url = mangas.xpath(".//a/@href").get()
            
            yield response.follow(url = manga_url, callback = self.parse_manga, meta={'title' : title})

    def parse_manga(self,response):
        title = response.request.meta['title']
        chapters = response.xpath("//table[@class='d48']/tr[position()>1 or position()=last()]")

        for chapter in chapters:
            chapter_count = chapter.xpath(".//td[1]/a/text()").get()
            chapter_name = chapter.xpath(".//td[1]/text()[2]").get()
            chapter_url = chapter.xpath(".//td[1]/a/@href").get()
            date_uploaded = chapter.xpath(".//td[2]/text()").get()

            yield{
                'title':title,
                'chapter':f"{chapter_count} {chapter_name}",
                'date_Added':date_uploaded
            }

            yield response.follow(url = chapter_url, callback = self.parse_manga_chapter,meta={'page_no':1, 'actual_url': chapter_url} )

            
    
    def parse_manga_chapter(self,response):
        page_src = response.xpath("//img[@id='ci']/@src").get()
        actual_url = response.url
        page_no = response.request.meta['page_no']
        yield{
            "image_src":page_src
        }
        
        page_no = page_no+1
        
        next_page_url = f"{actual_url}/{page_no}"
        print(next_page_url)
        while page_no < 5:
            yield scrapy.Request(next_page_url,callback=self.parse_manga_chapter,meta={'page_no':page_no, 'actual_url': actual_url})


        



        
    

            

