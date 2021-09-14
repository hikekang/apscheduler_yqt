#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/3 9:34
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : secodnd_data_utils.py
 Description:
 Software   : PyCharm
"""
import requests
from gne import  GeneralNewsExtractor
import re
from utils.webdriverhelper import MyWebDriver
from utils.webdriverhelper import WebDriverHelper
import time
from fake_useragent import UserAgent
from lxml import etree
extractor=GeneralNewsExtractor()
webdriver = WebDriverHelper.init_webdriver(is_headless=True, is_hide_image=True)
# webdriver = WebDriverHelper.init_webdriver(is_headless=False, is_hide_image=True)

def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
def crawl_second_by_requests(url:str):
    """

    :param url:
    :return:
    """
    try:
        proxy={"https":None,"http":None}
        header={
            "User-Agent":UserAgent().random
            # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        html = requests.get(url,proxies=proxy,headers=header)
        html_content = html.content.decode('utf-8')
        content = filter_emoji(extractor.extract(html_content, title_xpath='//html/text()')['content'])
        content+="<requests hidden>\n【只使用request抓取】</requests>"
        print("通过requests抓取",url)
    except Exception as e:
        print(e)
        content=crawl_second_by_webdriver(url)
        content+="<resuerst+selenium hidden>resuerst+selenium</resuerst+selenium>"
    content += "<requests hidden>\n【通过request抓取】</requests>"
    return content

def xpath_url(webdriver):
    time.sleep(0.5)
    page_source=webdriver.page_source
    current_url=webdriver.current_url
    doc=etree.HTML(page_source)
    try:
        content=""
        # 西瓜视频
        if "www.ixigua.com" in current_url:
            content = ""
        # 微信公众号
        elif "mp.weixin.qq.com" in current_url:
            if "链接已过期" in page_source:
                content=""
            else:
                content = webdriver.find_element_by_xpath('//div[@id="page-content"]').text
        elif "www.163.com/dy/article" in  current_url:
            content = webdriver.find_element_by_xpath('//div[@class="post_body"]').text
        elif "kuaibao.qq.com" in current_url:
            content = webdriver.find_element_by_xpath('//article[@class="content"]').text
        elif "www.sohu.com/a" in webdriver.current_url:
            content = webdriver.find_element_by_xpath('//article[@class="article"]').text
        elif "www.360kuai.com" in  current_url:
            content = webdriver.find_element_by_xpath('//article[@class="article"]').text
        elif "view.inews.qq.com" in  current_url:
            content = webdriver.find_element_by_xpath('//div[@id="root"]').text
        # 网易
        elif "dy.163.com/dy/article" in  current_url:
            if (webdriver.title == "网易-404"):
                content = ""
            else:
                content = webdriver.find_element_by_xpath('//div[@class="post_body"]').text
        # 百家号
        elif "mbd.baidu.com" in  current_url:
            if "dtlandingsuper" in webdriver.current_url:
                content = doc.xpath('string(//div[@class="index-module_contentContainer_3mQeg"])')
            else:
                content = webdriver.find_element_by_xpath('//div[@class="index-module_articleWrap_2Zphx"]').text
        elif "toutiao" in  current_url:
            if webdriver.title == '404错误页':
                content = ""
            else:
                print("获取源码")
                page_source = webdriver.page_source
                content = filter_emoji(extractor.extract(page_source, title_xpath='//html/text()')['content'])
        # 黑猫投诉
        elif "tousu.sina.com.cn" in  current_url:
            question = webdriver.find_element_by_xpath('//div[@class="ts-d-question"]').text
            steplist = webdriver.find_element_by_xpath('//div[@class="ts-d-steplist"]').text
            content = question + steplist
        elif "www.chasfz.com" in current_url:
            content=doc.xpath('//div[@class="article_content"]')[0].xpath("string(.)")
        elif "wap.peopleapp.com" in current_url:
            print("xx")
            content=doc.xpath('string(//div[@class="article-wrapper"])')
        elif "www.xiaohongshu.com" in current_url:
            if "该笔记已被删除" in page_source:
                content=""
            else:
                content=doc.xpath('string(//div[@class="content"])')
        elif "www.laihema.com" in current_url:
            content=doc.xpath('string(//div[@class="entry-content"])')
        #     看点快报
        elif "kuaibao.qq.com" in current_url:
            if "404 not found" in webdriver.title:
                pass
            else:
                content=doc.xpath('string(//article[@class="content"])')
        else:
            print("获取源码")
            page_source = webdriver.page_source
            content = filter_emoji(extractor.extract(page_source, title_xpath='//html/text()')['content'])
    except Exception as e:
        content=""
    return content



def crawl_second_by_webdriver(url):
    try:
        js_web = 'window.open("%s");' % url
        print("打开网页")
        webdriver.execute_script(js_web)
        print("切换窗口")
        webdriver.switch_to.window(webdriver.window_handles[-1])
        time.sleep(1)
        content=xpath_url(webdriver)
    except Exception as e:
        content=""
    finally:
        print("关闭网页")
        webdriver.close()
        webdriver.switch_to.window(webdriver.window_handles[0])
        print("解析数据")
    return content
if __name__ == '__main__':
    # content=crawl_second_by_requests('http://mp.weixin.qq.com/s?__biz=Mzg3ODEyNDc2OA==&mid=2247490592&idx=5&sn=1573c68c7deafc51c87c07b26c0d7acf&scene=6#wechat_redirect&')[0]
    # content=crawl_second_by_requests('https://www.sohu.com/a/469928830_114731')
    # 微信公众号跳转链接
    # content=crawl_second_by_requests('https://bbs.lh168.net/forum.php?mod=viewthread&tid=13169444')
    # content=crawl_second_by_requests('https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9084830844246581814%22%7D&n_type=-1&p_from=-1')

    # content=crawl_second_by_requests('http://dy.163.com/v2/article/detail/GBG8628S05490OGG.html')
    # content=crawl_second_by_requests('http://kuaibao.qq.com/s/20210602A03ZM000')
    # content=crawl_second_by_requests('http://www.sohu.com/a/470036093_120145113')
    # content=crawl_second_by_requests('https://new.qq.com/rain/a/20210602A0B3HG00')
    # content=crawl_second_by_requests('https://zhuanlan.zhihu.com/p/377206711')
    # content=crawl_second_by_requests('https://www.360kuai.com/9f164ef5c9b47ef93')
    # content=crawl_second_by_webdriver('https://view.inews.qq.com/a/20210620A0174400')
    # content=crawl_second_by_webdriver('https://tousu.sina.com.cn/complaint/view/17354346525/')
    # content=crawl_second_by_requests('http://www.chasfz.com/html/20210801/43972.html')
    # content=crawl_second_by_requests('http://m.news.so.com/transcoding?url=http://zm.news.so.com/90d5c4b11ef450394d4bf652de8122b0')
    # content=crawl_second_by_requests('https://wap.peopleapp.com/article/rmh22409662/4155590')
    # content=crawl_second_by_requests('https://m.itouchtv.cn/article/d4367240ab84d494804b1307fd23af51')
    # content=crawl_second_by_requests('https://info.gf.com.cn/web/newInfo/index.html#/detail/610cbe73ec9cf100065a73c0')
    # content=crawl_second_by_requests('https://www.meipian.cn/3qr004ub')
    # content=crawl_second_by_requests('https://mbd.baidu.com/newspage/data/landingshare?context=%7b%22nid%22%3a%22news_9147762216948631057%22%7d')
    # content=crawl_second_by_requests('https://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_5729621519340477912')
    # content=crawl_second_by_requests('https://www.laihema.com/show/8865851.html')
    # content=crawl_second_by_requests('http://kuaibao.qq.com/s/20210806A0C8PH00')
    content=crawl_second_by_requests('https://new.qq.com/rain/a/20210801A08DO200')

    # content=crawl_second_by_requests('https://view.inews.qq.com/a/20210602A01BEQ00')
    # content=crawl_second_by_requests('http://dy.163.com/v2/article/detail/GBG8GJSS0521K988.html')
    # content=crawl_second_by_webdriver('http://mp.weixin.qq.com/s?__biz=Mzg3ODEyNDc2OA==&mid=2247490592&idx=5&sn=1573c68c7deafc51c87c07b26c0d7acf&scene=6#wechat_redirect&')[0]
    # content=crawl_second_by_webdriver('https://www.toutiao.com/i6978710463605375527/')
    # content=crawl_second_by_webdriver('http://dy.163.com/v2/article/detail/GBG8GJSS0521K988.html')
    # content=crawl_second_by_webdriver('https://www.toutiao.com/w/i1701452788290571/')
    # content=crawl_second_by_webdriver('http://m.uczzd.cn/ucnews/news?app=ucnews-iflow&aid=2250631052201981853')
    # content=crawl_second_by_webdriver('http://kuaibao.qq.com/s/20210803A082D400')
    # content=crawl_second_by_webdriver('https://www.laihema.com/show/8865851.html')
    # content=crawl_second_by_webdriver('https://www.laohu8.com/news/2156143252')
    # content=crawl_second_by_webdriver('https://new.qq.com/rain/a/20210808A0ADFX00')
    # content=crawl_second_by_webdriver('https://ishare.ifeng.com/c/s/88Z8JGOJf12')
    # content=crawl_second_by_webdriver('http://www.chasfz.com/html/20210801/43972.html')
    # content = crawl_second_by_webdriver('https://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_5729621519340477912')
    # content = crawl_second_by_webdriver('https://www.xiaohongshu.com/discovery/item/610a2cdf0000000021037c53')
    # content = crawl_second_by_webdriver('https://kuaibao.qq.com/s/20210805A00JI300')
    print(content)