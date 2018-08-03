# encoding: utf-8
import sys
import os
from workflow import web,Workflow3
import mvnstring as mstr
from datetime import datetime

def main(wf):
    query = wf.args[0]
    # 保存输入查询
    wf.setvar('q',query,persist = False)
    if os.getenv('source') == 'aliyun':
        AliyunMaven(wf).action(query)
    else:
        CentralMaven(wf).action(query)

    wf.warn_empty('No result found!','Try other inputs...',icon = 'wrong.png')

    wf.send_feedback()




class AliyunMaven(object):
    def __init__(self, wf):
        self.wf = wf

    def action(self, query):
        mvnjson = web.get(mstr.ALI_REP % query).json()
        items = mvnjson['object']
        for item in items:
            self._get_item_dic(item)

    def _get_item_dic(self,item):
        mvndic = {}
        mvndic['g'] = item['groupId']               # groupId
        mvndic['a'] = item['artifactId']            # artifactId
        mvndic['v'] = item['version']               # version
        self._append(mvndic)
    
    def _append(self, dic):
        group = (dic['g'], dic['a'], dic['v'])
        it = self.wf.add_item(
            title = '%s:%s:%s' % group,
            subtitle = '复制 Gradle 配置...',
            valid = True,
            arg = mstr.MVN_PTN % group,
            icon = 'icons/aliyun.png'
        )
        it.setvar('clip', '%s:%s:%s' % group)
        cmd = it.add_modifier('cmd','在 mvnrepository.com 中搜索...')
        cmd.setvar('url', mstr.MVN_REP % wf.getvar('q'))
        alt = it.add_modifier('alt','复制 maven 配置...')
        alt.setvar('clip', mstr.MVN_PTN % group)
        ctrl = it.add_modifier('ctrl', '在 mvnrepository.com 中查看详情...')
        ctrl.setvar('url', mstr.REPO_DETAIL % group)
        shift = it.add_modifier('shift','在 search.maven.org 中搜索...')
        shift.setvar('url', mstr.MVN_SERACH % wf.getvar('q'))


class CentralMaven(object):
    def __init__(self, wf):
        self.wf = wf

    def action(self, query):
        mvnjson = web.get(mstr.CEN_REP % query).json()
        items = mvnjson['response']['docs']
        for item in items:
            self._get_item_dic(item)

    def _get_item_dic(self,item):
        mvndic = {}
        mvndic['g'] = item['g']                 # groupId
        mvndic['a'] = item['a']                 # artifactId
        mvndic['v'] = item['latestVersion']     # version
        date = str(datetime.fromtimestamp(item['timestamp']/1000))
        mvndic['t'] = date[:-9]                 # yyyy-MM-dd
        self._append(mvndic)
    
    def _append(self, dic):
        group = (dic['g'], dic['a'], dic['v'])
        it = self.wf.add_item(
            title = '%s:%s:%s' % group,
            subtitle = 'update at %s' % dic['t'],
            valid = True,
            arg = mstr.MVN_PTN % group,
            icon = 'icons/central.png'
        )
        it.setvar('clip', '%s:%s:%s' % group)
        cmd = it.add_modifier('cmd','在 mvnrepository.com 中搜索...')
        cmd.setvar('url', mstr.MVN_REP % wf.getvar('q'))
        alt = it.add_modifier('alt','复制 maven 配置...')
        alt.setvar('clip', mstr.MVN_PTN % group)
        ctrl = it.add_modifier('ctrl', '在 mvnrepository.com 中查看详情...')
        ctrl.setvar('url', mstr.REPO_DETAIL % group)
        shift = it.add_modifier('shift','在 search.maven.org 中搜索...')
        shift.setvar('url', mstr.MVN_SERACH % wf.getvar('q'))


if __name__ == '__main__':
    wf = Workflow3()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
