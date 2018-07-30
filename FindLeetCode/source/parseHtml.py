#-*- coding:utf-8 -*-
import sys
from bs4 import BeautifulSoup
try:
    import cPickle as pickle
except ImportError:
    import pickle


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'default.html'
    soup = BeautifulSoup(open(filename), "html.parser",from_encoding="utf8")
    data_dic = {}
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        index,dic = parseTd(tds)
        data_dic[index] = dic
    with open('dumps.txt','wr') as f:
        pickle.dump(data_dic, f)
        

def parseTd(tds):
    index = tds[1].get_text()
    en_name = tds[2]['value']
    aTag = tds[2].a
    href = aTag['href']
    ch_name = aTag.get_text()
    percent = tds[4].get_text()
    level = tds[5].span.get_text()
    dic = {
        'index':index,
        'en_name':en_name,
        'path':href[10:],
        'ch_name':ch_name,
        'percent':percent,
        'level':level,
    }
    return index, dic


if __name__ == '__main__':
    main()