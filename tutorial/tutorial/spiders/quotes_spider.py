import scrapy
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def save_sheet(store, price):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./client_secret.json', scope)
    client = gspread.authorize(credentials)

    sheet = client.open("prices").sheet1

    # before
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)


    next_row = next_available_row(sheet)

    sheet.update_cell(next_row, 1, store)
    sheet.update_cell(next_row, 2, price)


    # after
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.americanas.com.br/busca/airpods'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        price = response.xpath('//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[1]/div/div[2]/a/section/div[2]/div[2]/div[2]/span/text()[2]').getall()
        print("jackson")
        print(price)
        text = price[0]
        page = 10
        save_sheet("americanas", text)
        filename = 'quotes.txt'
        with open(filename, 'w') as f:
            f.write(text)
        self.log('Saved file %s' % filename)
