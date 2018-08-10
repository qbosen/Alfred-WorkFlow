# encoding: utf-8
import sys
import os
from workflow import web, Workflow3, ICON_INFO
from bs4 import BeautifulSoup


def main(wf):
    query = wf.args[0]
    # 保存输入查询
    wf.setvar('q', query, persist=False)
    MavenRepo(wf).action(query)
    wf.warn_empty('No result found!', 'Try other inputs...', icon='wrong.png')
    wf.send_feedback()


class MavenRepo(object):
    def __init__(self, wf):
        self.base_url = "https://mvnrepository.com"
        self.search_url = "https://mvnrepository.com/search?q=%s"
        self.wf = wf

    def action(self, query):
        url = self.search_url % query
        search_page = BeautifulSoup(web.get(url).content, 'html.parser')
        items = search_page.find_all(class_="im")
        for item in items:
            # 过滤谷歌的广告
            if item.find('script'):
                continue
            self._get_item_dic(item)

    def _get_item_dic(self, item):
        icon_url = item.find('img')['src'].encode('utf-8')
        t_div = item.find(class_='im-title')
        title = t_div.a.get_text().encode('utf-8')
        detail_url = self.base_url + t_div.a['href'].encode('utf-8')
        usage = t_div.find(class_='im-usage').b.get_text().replace(',', '').encode('utf-8')
        sub_div = item.find(class_='im-subtitle').find_all('a')
        artifact_info = ' > '.join([t.get_text() for t in sub_div]).encode('utf-8')
        subtitle = 'Usage: %-9s %s' % (usage, artifact_info)
        message = {'title': title, 'icon_url': icon_url, 'detail_url': detail_url, 'subtitle': subtitle}
        self._append(message)

    def _append(self, dic):
        it = self.wf.add_item(
            title=dic['title'],
            subtitle=dic['subtitle'],
            valid=True,
            arg=dic['detail_url'],
            # icon=dic['icon_url'],
            icon=ICON_INFO,
        )
        cmd = it.add_modifier('cmd', '在 %s 中搜索...' % self.base_url)
        cmd.setvar('url', self.search_url % wf.getvar('q'))


if __name__ == '__main__':
    wf = Workflow3()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
