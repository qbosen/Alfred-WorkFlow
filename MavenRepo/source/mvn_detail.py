# encoding: utf-8
import sys
import os
from workflow import web, Workflow3, ICON_INFO
from bs4 import BeautifulSoup
from datetime import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

detail_url = 'https://mvnrepository.com/artifact/'
maven_config = \
    '<dependency>\n\t<groupId>%s</groupId>\n\t<artifactId>%s</artifactId>\n\t<version>%s</version>\n</dependency>'
gradle_config = "compile group: '%s', name: '%s', version: '%s'"


def main(wf):
    query = wf.args[1] if (len(wf.args) > 1) else None
    log.info("query:" + str(query))

    gid = '{}:{}'.format(os.getenv('group'), os.getenv('artifact'))
    cache = CacheDumps('dumps.mvn')
    RepoDetail(wf, cache, gid).get_items().filter_and_append(query)

    wf.warn_empty('No result found!', 'Try other inputs...', icon='wrong.png')
    wf.send_feedback()


class CacheDumps(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.dumps = {}
        self.period = int(os.getenv('cache_days') or '0')
        self.cache_open = self.period > 0

    def load_dumps(self):
        if self.cache_open:
            try:
                with open(self.file_name, "rb") as f:
                    self.dumps = pickle.loads(f.read())
                    log.info('load cache')
            except Exception as e:
                log.warn(e)
        return self

    def get_data(self, gid):
        if not self.cache_open:
            return []

        if gid not in self.dumps:
            return []
        days_from_last = (datetime.now() - self.dumps[gid]['time']).days
        log.info("days from last update / setting period : %s / %s" % (days_from_last, self.period))

        return self.dumps[gid]['data'] if days_from_last < self.period else []

    def write_dumps(self, gid, item_list):
        if not self.cache_open:
            return
        self.dumps[gid] = {'time': datetime.now(), 'data': item_list}
        with open(self.file_name, 'wr') as f:
            pickle.dump(self.dumps, f)
            log.info('write cache')


class RepoDetail(object):
    def __init__(self, wf, cache, gid):
        self.wf = wf
        self.cache = cache
        self.gid = gid
        self.group, self.artifact = gid.split(':')
        self.big_step = self.get_step_version()
        self.url = '%s%s/%s' % (detail_url, self.group, self.artifact)
        self.items = []

    @staticmethod
    def get_step_version():
        step = os.getenv('step_version') or ''
        false_set = {'0', 'false', 'False', '', 'null', 'None'}
        return False if step in false_set else True

    def get_items(self):
        data_list = self.cache.load_dumps().get_data(self.gid)
        if len(data_list):
            self.items = data_list
        else:
            self._from_url()
            self.cache.write_dumps(self.gid, self.items)
        return self

    def filter_and_append(self, _filter):
        def key_for_dic(dic):
            return dic['version']

        its = self.wf.filter(_filter, self.items, key_for_dic)
        for it in its:
            self._append_wf(it)
        return self

    def _from_url(self):
        content = web.get(self.url).content
        search_page = BeautifulSoup(content, 'html.parser')
        big_versions = search_page.find('table', class_="grid versions").find_all('tbody')

        for big_version in big_versions:
            self._parse_version_block(big_version)

    def _parse_version_block(self, big_version):
        """
        parse a big version block
        if 'big_step' then only parse the newest version
        """
        small_versions = big_version.find_all('tr')
        if self.big_step:
            self._parse_version_detail(small_versions[0])
        else:
            for version in small_versions:
                self._parse_version_detail(version)

    def _parse_version_detail(self, block):
        def td_but_no_class(tag):
            return not tag.has_attr('rowspan') and tag.name == 'td'

        tds = block.find_all(td_but_no_class)
        version = tds[0].get_text().encode('utf-8')
        usage = tds[2].get_text().replace(',', '').encode('utf-8')
        date = tds[3].get_text().encode('utf-8')
        info = (self.group, self.artifact, version)
        self.items.append({
            'version': version,
            'usage': usage,
            'date': date,
            'info': info,
        })

    def _append_wf(self, dic):
        info = dic['info']
        it = self.wf.add_item(
            title='Version: %-20s Usage: %s ' % (dic['version'], dic['usage']),
            subtitle='%s:%s  Update: %s' % (self.group, self.artifact, dic['date']),
            valid=True,
            arg='%s:%s:%s' % info,
            # icon=:dic['icon_url'],
            icon=ICON_INFO,
        )
        it.setvar('clip', '%s:%s:%s' % info)
        cmd = it.add_modifier('cmd', 'Open in detail page...')
        cmd.setvar('url', self.url)
        alt = it.add_modifier('alt', 'Copy maven configuration...')
        alt.setvar('clip', maven_config % info)
        ctrl = it.add_modifier('ctrl', 'Copy gradle configuration...')
        ctrl.setvar('clip', gradle_config % info)


if __name__ == '__main__':
    wf = Workflow3()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
