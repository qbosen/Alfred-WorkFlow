# encoding: utf-8
import sys
from workflow import Workflow,web
import urls
try:
    import cPickle as pickle
except ImportError:
    import pickle

def main(wf):
    search = wf.args[0]
    # option + b 用于分割输入输出
    symbol = u'∫'
    qlist = query(search)
    dicBook = loadDumps()
    hasResult = False
    for item in qlist:
        if dicBook.has_key(item):
            hasResult = True
            addDicItem(wf, dicBook[item], search, symbol)

    if not hasResult:
        wf.add_item(
            title = u'没有匹配的结果', 
            subtitle = u'在 leetcode.cn 中搜索...', 
            icon = 'icon/wrong.png', 
            valid = True,
            arg = '%s%s%s'% (search, symbol,'')
        )

    wf.send_feedback()

def query(qstr):
    text = web.get(urls.QUERY_CN % qstr).text[1:-1]
    qlist = text.encode('utf8').split(',')
    return qlist

def loadDumps():
    dic = pickle.load(open('dumps.txt','r'))
    return dic

def addDicItem(wf, dic, search, symbol):
    icon_dic = {
        u'简单' : 'icon/easy.png',
        u'中等' : 'icon/medium.png',
        u'困难' : 'icon/hard.png',
    }
    wf.add_item(
        title = '[%s] %s' % (dic['index'], dic['ch_name']),
        # subtitle = '[%s] %s %s' % (dic['level'], dic['en_name'], dic['percent']),
        subtitle = '[%s] %s ' % (dic['percent'], dic['en_name']),
        arg = '%s%s%s'% (search, symbol, dic['path']),
        valid = True,
        icon = icon_dic[dic['level']]
    )

if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))