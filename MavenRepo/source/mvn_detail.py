# encoding: utf-8
import sys
import os
from workflow import web, Workflow3, ICON_INFO
from bs4 import BeautifulSoup

detail_url = 'https://mvnrepository.com/artifact/'
maven_config = \
    '<dependency>\n\t<groupId>%s</groupId>\n\t<artifactId>%s</artifactId>\n\t<version>%s</version>\n</dependency>'
gradle_config = "compile group: '%s', name: '%s', version: '%s'"


def main(wf):
    group = os.getenv('group')
    artifact = os.getenv('artifact')
    RepoDetail(wf, group, artifact).action()
    wf.warn_empty('No result found!', 'Try other inputs...', icon='wrong.png')
    wf.send_feedback()


class RepoDetail(object):
    def __init__(self, wf, group, artifact):
        self.wf = wf
        self.group = group
        self.artifact = artifact
        self.big_step = self.get_step_version()
        self.url = '%s%s/%s' % (detail_url, group, artifact)
        log.info('url:' + self.url)
        log.info('step:' + str(self.big_step))

    @staticmethod
    def get_step_version():
        step = os.getenv('step_version') or ''
        false_set = {'0', 'false', 'False', '', 'null', 'None'}
        return False if step in false_set else True

    def action(self):
        content = web.get(self.url).content
        search_page = BeautifulSoup(content, 'html.parser')
        big_versions = search_page.find('table', class_="grid versions").find_all('tbody')

        for big_version in big_versions:
            self._parse_version_block(big_version)

    def _parse_version_block(self, big_version):
        small_versions = big_version.find_all('tr')
        if self.big_step:
            self._parse_tr_and_append(small_versions[0])
        else:
            for version in small_versions:
                self._parse_tr_and_append(version)

    def _parse_tr_and_append(self, block):
        def td_but_no_class(tag):
            return not tag.has_attr('rowspan') and tag.name == 'td'

        tds = block.find_all(td_but_no_class)
        version = tds[0].get_text().encode('utf-8')
        usage = tds[2].get_text().replace(',', '').encode('utf-8')
        date = tds[3].get_text().encode('utf-8')
        info = (self.group, self.artifact, version)
        it = self.wf.add_item(
            title='Version: %-20s Usage: %s ' % (version, usage),
            subtitle='%s:%s  Update: %s' % (self.group, self.artifact, date),
            valid=True,
            arg='%s:%s:%s' % info,
            # icon=dic['icon_url'],
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
