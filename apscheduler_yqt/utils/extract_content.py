# -*- coding: utf-8 -*-
"""
   File Name：     extract_content
   Description :
   Author :       hike
   time：          2021/4/28 10:27
"""
from gne import GeneralNewsExtractor
def extract_content(html):
    extractor=GeneralNewsExtractor()
    r=extractor.extract(html)
    return r['content']