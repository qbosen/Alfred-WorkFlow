# coding=utf-8
import re
import urllib2
from settings import detail_url


def html_parse(text):
    mapping = {
        '&quot;': '"',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&circ;': '^',
        '&tilde;': '~',
        '&nbsp;': ' ',
    }
    text = text.replace('&amp;', '&')
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


class DescriptionParser(object):
    def __init__(self):
        self._title = ''
        self._content = ''

    def parse(self, path):
        url = detail_url % path
        text = urllib2.urlopen(url).read()
        _title = re.search(r'<title>(\S+).*</title>', text).group(1)
        self._title = html_parse(_title)
        _content = re.search(r'<meta name="description" content="(.*?)"\s*/>', text, re.S).group(1)
        self._content = html_parse(_content)
        return self

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content


if __name__ == '__main__':
    url2 = 'https://leetcode-cn.com/problems/add-two-numbers/description/'
    dp = DescriptionParser().parse(url2)
    print dp.content
    print dp.title
