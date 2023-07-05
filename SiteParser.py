from bs4 import BeautifulSoup as bs
import textwrap


class SiteParser:
    _max_text_length = 80

    def __init__(self, html):
        self._html = html
        self._article_tag = None
        self._article_class = None
        self._article_itemprop = None
        self._title_tag = None
        self._title_class = None
        self._title_itemprop = None
        self._content_tag = None
        self._content_class = None
        self._content_itemprop = None
        self._content_divs = []

    @property
    def article_tag(self):
        return self._article_tag

    @article_tag.setter
    def article_tag(self, value):
        self._article_tag = value

    @property
    def article_class(self):
        return self._article_class

    @article_class.setter
    def article_class(self, value):
        self._article_class = value

    @property
    def article_itemprop(self):
        return self._article_itemprop

    @article_itemprop.setter
    def article_itemprop(self, value):
        self._article_itemprop = value

    @property
    def title_tag(self):
        return self._title_tag

    @title_tag.setter
    def title_tag(self, value):
        self._title_tag = value

    @property
    def title_class(self):
        return self._title_class

    @title_class.setter
    def title_class(self, value):
        self._title_class = value

    @property
    def title_itemprop(self):
        return self._title_itemprop

    @title_itemprop.setter
    def title_itemprop(self, value):
        self._title_itemprop = value

    @property
    def content_tag(self):
        return self._content_tag

    @content_tag.setter
    def content_tag(self, value):
        self._content_tag = value

    @property
    def content_class(self):
        return self._content_class

    @content_class.setter
    def content_class(self, value):
        self._content_class = value

    @property
    def content_itemprop(self):
        return self._content_itemprop

    @content_itemprop.setter
    def content_itemprop(self, value):
        self._content_itemprop = value

    @property
    def content_divs(self):
        return self._content_divs

    @content_divs.setter
    def content_divs(self, value):
        self._content_divs = value

    def __wrap_text(self, long_text: str):
        wrapped_text = '\n'.join(textwrap.wrap(long_text, self._max_text_length))
        return wrapped_text

    def parse(self):
        parser = bs(self._html, "html.parser")
        result = ''

        article_element = None
        if self.article_class:
            article_element = parser.find(self.article_tag, attrs={'class': self.article_class})
        elif self.article_itemprop:
            article_element = parser.find(self.article_tag, itemprop=self.article_itemprop)
        if not article_element:
            raise Exception('Не нейден блок статьи.')

        title_element = None
        if self.title_class:
            title_element = article_element.find(self.title_tag, attrs={'class': self.title_class})
        elif self.title_itemprop:
            title_element = article_element.find(self.title_tag, itemprop=self.title_itemprop)
        if not title_element:
            raise Exception('Не нейден заголовок статьи.')

        result += self.__wrap_text(title_element.text)

        content_element = None
        if self.content_class:
            content_element = article_element.find(self.content_tag, attrs={'class': self.content_class})
        elif self.content_itemprop:
            content_element = article_element.find(self.content_tag, itemprop=self.content_itemprop)
        if not content_element:
            raise Exception('Не нейдено содержимое статьи.')

        for child in content_element:
            if child.name in self.content_divs:
                for a_tag in child.find_all('a'):
                    a_tag.string = '[{}]'.format(a_tag.text)
                result += '\n\n'
                result += self.__wrap_text(child.text)

        return result
