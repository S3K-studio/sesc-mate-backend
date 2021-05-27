from typing import Dict, List
from urllib import request
from bs4 import BeautifulSoup
import bs4


class NewsJson:
    __image: str
    __date: str
    __title: str
    __body: str
    __link: str

    def __init__(self, image: str, date: str, title: str, body: str, link: str):
        self.__image = image
        self.__date = date
        self.__title = title
        self.__body = body
        self.__link = link

    def serialise(self) -> Dict[str, str]:
        """News serializer"""
        return {
            'image': self.__image,
            'date': self.__date,
            'title': self.__title,
            'body': self.__body,
            'link': self.__link
        }


class NewsParser:
    __beautiful_soup_object: BeautifulSoup
    __page_html: str

    def __init__(self, html_code):
        self.__page_html = html_code

    def get_unique_data(self) -> str:
        self.__beautiful_soup_object: BeautifulSoup = BeautifulSoup(self.__page_html, features="html.parser")
        return str(
            self.__beautiful_soup_object.find('div', {'class': 'frame frame-default frame-type-list frame-layout-0',
                                                      'id': 'c190'}))

    def __get_all_news(self, bs4_object: BeautifulSoup) -> bs4.ResultSet:
        return bs4_object.find_all('div', {'class': 'col'})

    def __parse_news(self, news_list: bs4.ResultSet) -> List[Dict[str, str]]:
        parsed_news: List[Dict[str, str]] = []
        for item in news_list:
            image: str = item.find('img')['src']
            date: str = item.find('p', {'class': 'date'}).text
            title: str = item.find('h4').text
            body: str = item.find('p', {'class': 'description'}).text
            link: str = item.find('a')['href']
            news: NewsJson = NewsJson(image, date, title, body, link)
            parsed_news.append(news.serialise())
        return parsed_news

    def parse(self) -> List[Dict[str, str]]:
        """Method for getting JSON with all news"""

        div_with_news: str = self.get_unique_data()  # Get div with all news
        news_list: bs4.ResultSet = self.__get_all_news(
            BeautifulSoup(div_with_news, features="html.parser"))  # Get divs for each news
        parsed_news: List[Dict[str, str]] = self.__parse_news(news_list)  # Parse list of news divs
        return parsed_news


# For tests
if __name__ == '__main__':
    page = request.urlopen('https://lyceum.urfu.ru/news')
    encoded_html = page.read()
    page_html = encoded_html.decode('utf-8')
    page.close()
    parser = NewsParser(page_html)
    print(parser.get_unique_data())
    print(parser.parse())
