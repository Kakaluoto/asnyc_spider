# coding-utf-8
from baiduspider import BaiduSpider
from pprint import pprint
from fake_useragent import UserAgent
import random
import asyncio
import cv2
from ip_pool import ProxyPool
from async_spider import AsyncSpider
from image_selector import ImageSelector
import os

cookie = 'BIDUPSID=6D7E8E5D2F07EE9D08A8080FC3938C06; PSTM=1632104737; __yjs_duid=1_3adeed2ed557c331f3bb9e520f6bf7191632104785760; BD_UPN=12314753; BDSFRCVID=OoCOJeCmHxjmO3nDa2s0b5HDoeKK0gOTHllnXoCsam76i_tVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFsQf5RB2Q-XPoO3KtMObnvy-cz0RFVjt7R2-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9Qg-JKpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5thj6PVKgTa54cbb4o2WbCQ2-bz8pcN2b5oQT8hK-6qBnk856na_lngab5vOIJTXpOUWJDkXpJvQnJjt2JxaqRC5-cmqp5jDh3MQ5tyMl7me4ROfgTy0hvctb3cShPmQMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDHt8JT-tJJ3aQ5rtKRTffjrnhPF3eMIUXP6-hnjy3bREQpcKWPnJOx7Pjf7UhPLUyN3MWh3Ry6r42-39LPO2hpRjyxv4bnIrKPoxJpOJ3n7eBtnnHR7Wbh5vbURvDP-g3-AJ0U5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtI0hMCvPKITD-tFO5eT22-us2n7m2hcHMPoosIJuKM6-y-7XD-5atxvRaKTiaKJjBMbUotoHXnJi0btQDPvxBf7p55QTQh5TtUJMsKORMR7Tqt4be-oyKMnitKv9-pP23pQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuD6A-D5cWjaDs-bbfHj7y0t-E5n7bD6rkbJ83XP4dXP6-3-r7MIQL2KO83nDKqIJPjf7UhPLUyN3MWh37aIJXhn7n-bjVMIQYBnO4y4Ldj4oxJpOJ5JbMopvaKf5pD-ovbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCIaMIOP; BDSFRCVID_BFESS=OoCOJeCmHxjmO3nDa2s0b5HDoeKK0gOTHllnXoCsam76i_tVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvDqTrP-trf5DCShUFsQf5RB2Q-XPoO3KtMObnvy-cz0RFVjt7R2-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9Qg-JKpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5thj6PVKgTa54cbb4o2WbCQ2-bz8pcN2b5oQT8hK-6qBnk856na_lngab5vOIJTXpOUWJDkXpJvQnJjt2JxaqRC5-cmqp5jDh3MQ5tyMl7me4ROfgTy0hvctb3cShPmQMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDHt8JT-tJJ3aQ5rtKRTffjrnhPF3eMIUXP6-hnjy3bREQpcKWPnJOx7Pjf7UhPLUyN3MWh3Ry6r42-39LPO2hpRjyxv4bnIrKPoxJpOJ3n7eBtnnHR7Wbh5vbURvDP-g3-AJ0U5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtI0hMCvPKITD-tFO5eT22-us2n7m2hcHMPoosIJuKM6-y-7XD-5atxvRaKTiaKJjBMbUotoHXnJi0btQDPvxBf7p55QTQh5TtUJMsKORMR7Tqt4be-oyKMnitKv9-pP23pQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuD6A-D5cWjaDs-bbfHj7y0t-E5n7bD6rkbJ83XP4dXP6-3-r7MIQL2KO83nDKqIJPjf7UhPLUyN3MWh37aIJXhn7n-bjVMIQYBnO4y4Ldj4oxJpOJ5JbMopvaKf5pD-ovbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCIaMIOP; H_WISE_SIDS=110085_127969_153067_179346_184716_189659_190616_191067_191245_194085_194511_195343_196425_196528_197241_197711_197956_198263_199023_199571_200434_200596_200735_201108_201601_201700_202058_202759_202847_202911_203504_203606_203886_204098_204233_204255_204305_204675_204717_204760_204817_204823_204860_204909_204973_205087_205218_205235_205426_205484_205548_205553_205690_205831_205958_206008_206099_206120_206251_206283_206516_206705_206870_206897_207126_207234_207272_207364_207497_207604; BDUSS=dwQ1NRd3psS2NWQVlKSTRDdTJIYmtrMk43M1E3RGM2d0puVUxXODZneG9TMlppSVFBQUFBJCQAAAAAAAAAAAEAAAA~b41-MTA1MjE3Njg3M7-oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGi-PmJovj5iVm; BDUSS_BFESS=dwQ1NRd3psS2NWQVlKSTRDdTJIYmtrMk43M1E3RGM2d0puVUxXODZneG9TMlppSVFBQUFBJCQAAAAAAAAAAAEAAAA~b41-MTA1MjE3Njg3M7-oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGi-PmJovj5iVm; BAIDUID=4DED946BD1B5CFC32FBD06173C18774F:SL=0:NR=10:FG=1; delPer=0; BD_CK_SAM=1; ZD_ENTRY=bing; BD_HOME=1; H_PS_PSSID=35836_31254_36086_36167_34584_36142_36121_36073_36126_36225_26350_36112_36093_36061; RT="z=1&dm=baidu.com&si=3jhtuchb4mv&ss=l1p2vdiv&sl=4&tt=1ir&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=10ma&ul=11ft&hd=11g1"; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; PSINO=6; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm; BDRCVFR[CLK3Lyfkr9D]=mk3SLVN4HKm; ab_sr=1.0.1_ZGY1OTA0MzhiZmRjOWQ0YmJkOGIzOWYwMjhjOTA5ZTQ3NGY5ODNmYjk2ZmFkZTgwZTE3MmJjZDNhODRiMDkyYjczZDgyOGFjMjljM2UwNWQ5N2M5N2RlZDBmODdiY2Q5OTE4ZGU4YjA3N2VkZTRhNjcwZmNjNjg4MWU1ODc1MjYxZTVhOWYxZGE1ZDgxY2QxZjFhYWVlNThlZmJiNGIwNmJjMzlhZTUyNzliYzI5ZmI1YTgwNmY0NDA5NTMzMTg0; BAIDUID_BFESS=4DED946BD1B5CFC32FBD06173C18774F:SL=0:NR=10:FG=1; channel=baiduspider.github.io; sug=3; sugstore=0; ORIGIN=2; bdime=0; H_PS_645EC=c72bkbWXfQcvPZa9uL9F9uQq+Y6VmFfhqJ7zmLjDgO7PsE0nZImUyjlMyLI; BA_HECTOR=000hag810l802480pd1h5351c0r; baikeVisitId=957616f1-00aa-4352-a374-1d120b7c259f'
proxypool = ProxyPool()
proxies = proxypool.get_useful_ip()


def get_downloadlink(keyword="金枪鱼", cookie=None, proxies=None, num=180, start_page=1):
    """

    :param keyword: 百度搜索关键词
    :param cookie: 添加自己的cookie，用来提供给baiduspider生成不同的cookie
    :param proxies: 代理IP列表
    :param num: 需要爬取的图片数
    :param start_page: 从百度搜索页面的第几页开始搜索
    :return: 返回可直接下载的所有图片链接
    """
    if cookie is not None:
        spider = BaiduSpider(cookie=cookie)
    else:
        spider = BaiduSpider()
    spider.headers["Connection"] = "close"

    result = []
    num_pages = int(num / 60)
    for page in range(start_page, start_page + num_pages):
        while True:
            proxy = random.choice(proxies)  # 随机选一个IP
            spider.headers["User-Agent"] = UserAgent(use_cache_server=False).random  # 随机生成user-agent
            try:  # search_pic_by_hy是我自己复制了一份修改的
                result += spider.search_pic_by_hy(keyword, proxies=proxy, pn=page + 1, verify=False).plain
                break
            except Exception as e:
                print("尝试重新获取图片链接")
                continue

    return result


result = get_downloadlink(cookie=cookie, proxies=proxies, num=600)
print(len(result))
# aspider = AsyncSpider(proxies=proxies)
aspider = AsyncSpider()
download_task = aspider.run(url_list=result)
asyncio.run(download_task)
path = r"./img"
img_path_list = os.listdir(path)
img_selector = ImageSelector(img_path=path)
# for img_name in img_path_list:
#     img_selector.select_function(img_name=img_name)
delete_list = img_selector.get_delete_list(max_workers=1000)
img_selector.delete_image(path=path, image_list=delete_list)
