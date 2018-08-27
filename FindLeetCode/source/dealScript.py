# coding=utf-8
import sys
import re

# 键位
cmd = "none"
content = "{query}"
# 约定的输出格式
regx = r'(.*)∫(.*)'

QUERY_CN = "https://leetcode-cn.com/problems/api/filter-questions/%s"
QUERY = "https://leetcode.com/problems/api/filter-questions/%s"

SEARCH_CN = "https://leetcode-cn.com/problemset/all/?search=%s"
SEARCH = "https://leetcode.com/problemset/all/?search=%s"

DESCRIPTION = "https://leetcode.com/problems/%s/description/"
DESCRIPTION_CN = "https://leetcode-cn.com/problems/%s/description/"

DISCUSS = "https://leetcode.com/problems/%s/discuss/"

m = re.match(regx, content)
if m:
    query, title = m.group(1), m.group(2)
else:
    query, title = '', ''

hasItem = title != ''
if hasItem:
    if cmd == 'alt':
        url = DISCUSS % title
    elif cmd == 'cmd':
        url = SEARCH_CN % query
    else:
        url = DESCRIPTION_CN % title
else:
    if cmd == 'alt':
        url = SEARCH % query
    else:
        url = SEARCH_CN % query

sys.stdout.write(url)
