import bs4
from html_sanitizer import Sanitizer


class AnnouncementsParser:
    """Класс парсера для получения объявлений
    Есть только один метод - get_news()"""

    def __init__(self, html):
        self.html = html

    def get_unique_data(self) -> str:
        soup: bs4.BeautifulSoup
        soup = bs4.BeautifulSoup(self.html, 'lxml')

        section: bs4.element.Tag
        section = soup.find('section', {'class': 'row announcements'})
        ads = section.findAll('div', {'class': 'description-wrapper'})

        # Список тегов с объявлениями
        ads: bs4.element.ResultSet

        return str(ads)

    @staticmethod
    def make_json(take_ads) -> list:
        # json из div

        header: str
        date: str

        ads = bs4.BeautifulSoup(take_ads, 'lxml')
        ads = ads.findAll('div', {'class': 'description-wrapper'})

        # Итоговый json (cписок)
        news: list
        news = []

        sanitizer = Sanitizer()

        # Формирование json для каждого объявления
        ad: bs4.element.Tag
        for ad in ads:
            # Заголовок объявления
            header_node = ad.find('h4')
            header_text = header_node.text
            header_node.decompose()
            # Весь HTML объявления
            content: str = sanitizer.sanitize(str(ad))
            # Replace relative path
            content = content.replace('href="/', 'href="https://lyceum.urfu.ru/')
            content = content.replace('target=\"_blank\" ', '')
            content = content.replace('target=\"_self\" ', '')
            content = content.replace('target=\"_parent\" ', '')
            content = content.replace('target=\"_top\" ', '')
            content = content.replace('<a', '<a target=\"_blank\"')

            new = {
                'header': header_text,
                'content': content,
                'trustedOrigin': False
            }
            news.append(new)

        return news

    def parse(self) -> list:
        """Метод для получения объявлений"""

        # Список тегов с объявлениями
        ads: str
        ads = self.get_unique_data()

        # Итоговый json
        news: list
        news = self.make_json(ads)

        return news
