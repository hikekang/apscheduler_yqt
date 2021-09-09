# -*- coding: utf-8 -*-
"""
   File Name：     pyquerytest
   Description :
   Author :       hike
   time：          2021/4/22 17:48
"""
from pyquery import PyQuery as pq
html = """
<td ng-if="icc.commentPojo==null" class="ng-scope">
					<div class="profile-title inline-block">
								<!-- 标题或者作者 start -->
								<!-- ngIf: icc.originType=='wb'&& icc.captureWebsiteName=='微博头条' -->
								<!-- ngIf: icc.originType=='wb'&&icc.author=='' && icc.captureWebsiteName!='微博头条' -->
								<!-- ngIf: icc.originType=='wb'&&icc.author!=''&&icc.author!=null && icc.captureWebsiteName!='微博头条' --><a href="" value="516191451276474344513526" ng-click="getDetail(icc,currentKeyword);" ng-if="icc.originType=='wb'&amp;&amp;icc.author!=''&amp;&amp;icc.author!=null &amp;&amp; icc.captureWebsiteName!='微博头条'" ng-bind="icc.author" class="ng-binding ng-scope">左手的诗人</a><!-- end ngIf: icc.originType=='wb'&&icc.author!=''&&icc.author!=null && icc.captureWebsiteName!='微博头条' -->
								<!-- ngIf: icc.originType=='wx' -->
								
								<!-- ngIf: icc.originType!='wb' && icc.originType!='wx' -->
								<!-- ngIf: icc.originType=='sp'&&icc.title=='' && icc.author!='' -->
								<!-- 标题或者作者 end -->

								<!-- 标属性 start -->
								<div class="inline-block select-wrapper bar-select" ng-show="view.resultPresent != 3">
									<div class="sensitive-status-wrapper p-r">
                                        <div class="sensitive-status-content mg ng-hide" data-toggle="dropdown" ng-show="icc.customFlag1 == 1 || icc.customFlag1 == 2 || icc.customFlag1 == 3">
                                            <span class="inline-block">敏感</span>
                                            <span class="inline-block fa"></span>
                                        </div>
                                        <div class="sensitive-status-content fmg" data-toggle="dropdown" ng-show="icc.customFlag1 == 4">
                                            <span class="inline-block">非敏感</span>
                                            <span class="inline-block fa"></span>
                                        </div>
                                        <div class="sensitive-status-content zx ng-hide" data-toggle="dropdown" ng-show="icc.customFlag1 == 5">
                                            <span class="inline-block">中性</span>
                                            <span class="inline-block fa"></span>
                                        </div>
                                        <ul class="layout-frame sensitive-status-select font-size-12 dropdown-menu">
                                            <li class="mb5" ng-click="changeCustomFlag($event,icc,1)">
                                                敏感
                                            </li>
											<li class="mb5" ng-click="changeCustomFlag($event,icc,5);">
												中性
											</li>
                                            <li class="mb5" ng-click="changeCustomFlag($event,icc,2);">
                                                非敏感
                                            </li>
                                        </ul>
										<!-- <ul class="layout-frame sensitive-status-select hide" id="sensitive-status-select_{{icc.id}}">
											<li class="mb5 " ng-click="changeCustomFlag($event,icc,1);" ng-show="icc.customFlag1 == 4">敏感</li>
											<li class="" ng-click="changeCustomFlag($event,icc,2);" ng-show="icc.customFlag1 == 1 || icc.customFlag1 == 2 || icc.customFlag1 == 3">非敏感</li>
										</ul> -->
									</div>
								</div>
								
								<div class="inline-block select-wrapper bar-select">
									<div class="sensitive-status-wrapper p-r">
										<div class="sensitive-status-content font-size-0" ng-click="dataFeedback(icc);">
											<span class="inline-block">纠错</span>
										</div>
									</div>
								</div>
                                
								<!-- ngIf: icc.isWarning!=null&&icc.isWarning==2 -->

								<!-- <div class="inline-block yuanchuang-bg tip-bg vertical-align-middle" ng-if='(icc.captureWebsiteName=="新浪微博" || icc.originType=="wb" || icc.captureWebsiteName=="腾讯微博") && icc.repostsFlg==0'>原</div>
								<div class="inline-block zhuanfa-bg tip-bg vertical-align-middle" ng-if='(icc.captureWebsiteName=="新浪微博" || icc.originType=="wb" || icc.captureWebsiteName=="腾讯微博") && icc.repostsFlg!=0'>转</div>
								<div class="inline-block pinglun-bg tip-bg vertical-align-middle" ng-if='(icc.captureWebsiteName=="新浪微博" || icc.originType=="wb" || icc.captureWebsiteName=="腾讯微博") && icc.updateFilter==1'>更</div> -->
								<!-- 标属性 end -->
							</div>
</td>	
"""



doc=pq(html)
td_title=doc.find('td')
hh=doc.find('div.sensitive-status-wrapper.p-r:first-child>div.sensitive-status-content:not(.ng-hide)>span:first-child').text()

positive_dict = {
    "敏感": 0.1,
    "非敏感": 0.9,
    "中性": 0.5
}
# hi=doc.xpath('//div[contains(@class,"sensitive-status-content") and not (contains(@class,"ng-hide")]')
# print(hi)
print(hh.split()[0])
# print(positive_dict[hh])
# print(hh)