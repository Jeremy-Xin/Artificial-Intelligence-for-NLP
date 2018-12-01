import requests
from urllib.parse import quote

lines = {}
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
names = ['北京地铁1号线','北京地铁2号线','北京地铁4号线','北京地铁5号线','北京地铁6号线','北京地铁7号线','北京地铁8号线','北京地铁9号线','北京地铁10号线','北京地铁13号线','北京地铁14号线东段','北京地铁14号线西段','北京地铁15号线','北京地铁16号线','北京地铁八通线','北京地铁昌平线','北京地铁亦庄线','北京地铁房山线','北京地铁机场线','北京地铁s1线','北京地铁燕房线','北京地铁西郊线']
for name in names:
    try:
        url = 'https://baike.baidu.com/item/' + quote(name, 'gbk')
        res = s.get(url)
        f = open('output.html', 'wb')
        f.write(res.content)
        f.close()
        f = open('output.html', 'r')
        content = f.read()
        lines[name] = []
        from lxml import etree
        tree = etree.HTML(content)
        nodes = tree.xpath('//table[@data-sort]')
        for node in nodes:
            links = node.xpath('tr/td//a')
            if not links:
                links = links = node.xpath('tbody/tr/td//a')
            print(len(links))
            for l in links:
                text = l.xpath('text()')
                if not text:
                    continue
                text = text[0]
                if text.endswith('站'):
                    lines[name].append(text[:-1])
            if len(lines[name]) > 3:
                break
            else:
                lines[name] = []
    except:
        pass

import csv
with open('lines_crawled.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for key in lines:
        writer.writerow([key] + lines[key])