from parsel import Selector
import requests
from db.db_functions import init_db, fill_table

class Parser:
    URL = 'https://www.house.kg/snyat'

    def pagination(self, start=1, end=10):
        for page in range(start, end+1):
            yield f'{self.URL}?page={page}'


    def get_all_text(self, html = URL):
        return requests.get(f'{html}').text

    def get_headers(self):
        headers = []
        for url in self.pagination(1, 2):
            html = self.get_all_text(url)
            selector = Selector(text=html)
            houses = selector.css('p.title')
            for house in houses:
                header = house.css('a::text').get().strip()
                headers.append(header)
        return headers

    def get_prices(self):
        prices = []
        for url in self.pagination(1, 2):
            html = self.get_all_text(url)
            selector = Selector(text=html)
            price_divs = selector.css('div.listing-prices-block')
            for div in price_divs:
                price = div.css('div.price::text').get().strip()
                prices.append(price)
        return prices

    def get_adresses(self):
        addresses = []
        for url in self.pagination(1, 2):
            html = self.get_all_text(url)
            selector = Selector(text=html)
            divs = selector.css('div.left-side')
            for address_div in divs:
                '''Сделал так, потому что текст с дива не доставался'''
                address = address_div.css('.address').get()
                if address is not None:
                    address = address.split()
                    reformat_address = ''
                    for elem in address[5:-1]:
                        reformat_address += f'{elem} '
                    addresses.append(reformat_address)
        return addresses

    def get_descriptions(self):
        descriptions = []
        for url in self.pagination(1, 2):
            html = self.get_all_text(url)
            selector = Selector(text=html)
            descriptions_divs = selector.css('div.right-info')
            for div in descriptions_divs:
                description = div.css('div.description::text').get().strip()
                descriptions.append(description)
        return descriptions




if __name__ == '__main__':
    HouseKg = Parser()
    init_db()
    titles_list = HouseKg.get_headers()
    prices_list = HouseKg.get_prices()
    address_list = HouseKg.get_adresses()
    description_list = HouseKg.get_descriptions()
    for i in range(0, 21):
        title = titles_list[i]
        price = prices_list[i]
        address = address_list[i]
        description = description_list[i]
        if price is None:
            price = 'Null'
        if description is None:
            description = 'Null'
        if address is None:
            address = 'Null'
        if description is None:
            description = 'Null'
        init_db()
        try:
            fill_table(title, price, address, description)
        except:
            continue
