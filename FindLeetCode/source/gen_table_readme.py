# coding=utf-8
import cookielib
import json
import os
import re
import urllib2
import sys


try:
    import cPickle as pickle
except ImportError:
    import pickle


def create_table(data, qids):
    pattern = '| {} | {} | {} |'
    head_cn = pattern.format('题号', '标题', '标签')
    splitter = pattern.format(':---', ':---', ':---')
    content = head_cn + '\n' + splitter
    for id in qids:
        if id in data:
            detail = data[id]
            tags = ', '.join([tag['translatedName'] for tag in detail['topicTags']]).encode('utf-8')
            id_encode = id.encode('utf-8')
            title = '[{}][{:0>3}]'.format(detail['translatedTitle'].encode('utf-8'), id)
            content = content + '\n' + pattern.format(id_encode, title, tags)
    return content


def query():
    body = r'{"operationName":"getQuestionTranslation","variables":{},"query":"query getQuestionTranslation($lang: ' \
           r'String) {\n translations: allAppliedQuestionTranslations(lang: $lang) {\n question {\n questionId' \
           r'\n translatedTitle\n questionTitle\n difficulty\n stats\n questionTitleSlug\n topicTags{name\n ' \
           r'translatedName} }\n }\n}\n"} '

    cookie_jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
    base_url = 'https://leetcode-cn.com'
    request = urllib2.Request(base_url)
    urllib2.urlopen(request)
    cookies = dict((cookie.name, cookie.value) for cookie in cookie_jar)
    csrftoken = cookies['csrftoken']
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Referer': base_url,
        'Cookie': 'csrftoken=%s' % csrftoken
    }
    request = urllib2.Request('https://leetcode-cn.com/graphql', body, headers)
    response = urllib2.urlopen(request)
    data = json.load(response)

    def format_data(data_list):
        data_dic = {}
        for d in data_list:
            data_dic[d['question']['questionId']] = d['question']
        return data_dic

    return format_data(data['data']['translations'])


def save2dump(data):
    """
    replace the old dumps.txt generation way
    the dict format is somehow strange because it is compatible with the old codes
    :param data:
    :return:
    """
    dic = {}
    level_map = {'Easy': u'简单', 'Medium': u'中等', 'Hard': u'困难'}
    for q in data.values():
        stats = json.loads(q['stats'])
        index = q['questionId'].encode('utf-8')
        inner_dic = {
            'index': index,
            'en_name': q['questionTitle'].encode('utf-8'),
            'path': q['questionTitleSlug'].encode('utf-8'),
            'ch_name': q['translatedTitle'].encode('utf-8'),
            'percent': stats['acRate'].encode('utf-8'),
            'level': level_map[q['difficulty']].encode('utf-8'),
        }
        dic[index] = inner_dic

    with open('dumps.txt', 'wr') as f:
        pickle.dump(dic, f)
    print 'success update dumps.txt!'


def scan_path(src):
    def get_qids(path):
        ids = []
        pattern = re.compile(r'q0*(\d+)')
        files = sorted(os.listdir(path))
        for d in files:
            m = pattern.match(d)
            if m:
                ids.append(m.group(1))
        return ids

    easy_list = get_qids(os.path.join(src, 'easy'))
    medium_list = get_qids(os.path.join(src, 'medium'))
    hard_list = get_qids(os.path.join(src, 'hard'))
    return easy_list, medium_list, hard_list


def generate_file(full_path, content):
    with open(full_path, 'w') as f:
        f.write(content)
    print 'update file README.md'


class Gens(object):
    def __init__(self):
        self._data = query()

    def update_dumps(self):
        save2dump(self._data)

    def update_readme(self):
        def gen_url(level, qid):
            result = ''
            for id in qid:
                result += '[{:0>3}]: src/{}/q{:0>3}/README.md\n'.format(id, level, id)
            return result

        qids = list(scan_path(src_path))
        content = '## 简单\n\n{}\n\n## 中等\n\n{}\n\n## 困难\n\n{}\n\n'.format(*map(create_table, [self._data] * 3, qids))
        content += '<!-- 简单 -->\n{}\n\n<!-- 中等 -->\n{}\n\n<!-- 困难 -->\n{}\n\n'.format(
            *map(gen_url, ['easy', 'medium', 'hard'], qids))
        generate_file(os.path.join(src_path, os.pardir, 'README.md'), content)


if __name__ == '__main__':
    param = sys.argv[1]
    src_path = sys.argv[2]
    if param == 'update_dumps':
        Gens().update_dumps()
    elif param == 'update_readme':
        Gens().update_readme()
