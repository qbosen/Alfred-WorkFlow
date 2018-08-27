# coding: utf-8
import os
import sys
import urls

from workflow import Workflow3, web

try:
    import cPickle as pickle
except ImportError:
    import pickle


def main(wf):
    search = wf.args[0]
    wf.setvar('q', search, persist=False)
    q_list = query(search)
    q_dict = load_dumps()

    count = 0
    limit = os.getenv('limit') or '20'
    limit = int(limit)
    for item in q_list:
        if item in q_dict and count < limit:
            count = count + 1
            add_item(wf, q_dict[item])

    wf.warn_empty('No result found!', 'Try other inputs...', icon='icon/wrong.png')
    wf.send_feedback()


def query(q_str):
    text = web.get(urls.QUERY_CN % q_str).text[1:-1]
    q_list = text.encode('utf8').split(',')
    return q_list


def load_dumps():
    dic = pickle.load(open('dumps.txt', 'r'))
    return dic


def add_item(wf, dic):
    icon_dic = {
        u'简单': 'icon/easy.png',
        u'中等': 'icon/medium.png',
        u'困难': 'icon/hard.png',
    }
    level = dic['level'].decode('utf-8')
    it = wf.add_item(
        title='[%s] %s' % (dic['index'], dic['ch_name']),
        # subtitle = '[%s] %s %s' % (dic['level'], dic['en_name'], dic['percent']),
        subtitle='[%s] %s ' % (dic['percent'], dic['en_name']),
        arg=dic['index'],
        valid=True,
        icon=icon_dic[level]
    )
    it.setvar('url', urls.DESCRIPTION_CN % dic['path'])
    cmd = it.add_modifier('cmd', 'Searching in leetcode-cn.com...')
    cmd.setvar('url', urls.SEARCH_CN % wf.getvar('q'))
    alt = it.add_modifier('alt', 'Open discussion in leetcode.com...')
    alt.setvar('url', urls.DISCUSS % dic['path'])
    ctrl = it.add_modifier('ctrl', 'Generate files...')
    ctrl.setvar('index', dic['index'])


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
