# 发送请求模块
import requests
# 解析html工具 lxml pip install lxml
from lxml import etree
from time import sleep
import os

# 伪装自己
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Cookie': 'kg_mid=faeadeec7b2b18a0a3271146751a9a06; kg_dfid=0R7u9i1l4rNC1X3CQ34bWqce; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1666617860,1666696187; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1666703405'
}
# 获取英雄列表
hero_list_url = 'https://pvp.qq.com/web201605/js/herolist.json'
hero_list_resp = requests.get(hero_list_url, headers=headers)
for h in hero_list_resp.json():
    ename = h.get('ename')
    cname = h.get('cname')
    if not os.path.exists(cname):
        os.makedirs(cname)

# 访问英雄主页
    hero_info_url = f'https://pvp.qq.com/web201605/herodetail/{ename}.shtml'
    hero_info_resp = requests.get(hero_info_url, headers=headers)
    hero_info_resp.encoding = 'GBK'
    e = etree.HTML(hero_info_resp.text)
    names = e.xpath('//ul[@class="pic-pf-list pic-pf-list3"]/@data-imgname')[0]
    names = [name[0:name.index('&')] for name in names.split('|')]
# 发送请求
    for i, n in enumerate(names):
        resp = requests.get(
            f'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-{i+1}.jpg', headers=headers)

# 接受服务器响应的图片
# 保存图片
        with open(f'{cname}/{n}.jpg', 'wb') as f:
            f.write(resp.content)
            sleep(1)
            print(f'已下载-{cname}-{n}的皮肤')
