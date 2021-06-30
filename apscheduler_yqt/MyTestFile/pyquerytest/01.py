tdtitle="""
<td ng-if="icc.commentPojo==null" class="ng-scope">
					<div class="news-content font-size-0 text-left p-r p10" id="news-content_316214740215654652355411">
						<div class="info-label p-a ng-hide" ng-show="icc.readFlag=='1' &amp;&amp; view.resultPresent != 3">
							<div class="read-over p-a"></div>
						</div>
						<div class="inline-block" style="width: 34px;">
							<div class="inline-block profile-img-wrapper mb10" ng-click="getDetail(icc,currentKeyword);" style="cursor: pointer">
								<!-- ngIf: icc.profileImageUrl!= null && icc.profileImageUrl != '' --><img ng-if="icc.profileImageUrl!= null &amp;&amp; icc.profileImageUrl != ''" ng-src="https://cdn-iisstat-files.51wyq.cn/celebrity/2018071309550759.jpg" alt="" class="ng-scope" src="https://cdn-iisstat-files.51wyq.cn/celebrity/2018071309550759.jpg"><!-- end ngIf: icc.profileImageUrl!= null && icc.profileImageUrl != '' -->
							    <!-- ngIf: icc.originType=='wb'&&icc.captureWebsiteName=='新浪微博'&&icc.profileImageUrl==null||icc.originType=='wb'&&icc.captureWebsiteName=='新浪微博'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='sp'&&icc.profileImageUrl==null || icc.originType=='sp'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='wx'&&icc.profileImageUrl==null || icc.originType=='wx'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='xw'&&icc.profileImageUrl==null || icc.originType=='xw'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='lt'&&icc.profileImageUrl==null || icc.originType=='lt'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='bk'&&icc.profileImageUrl==null || icc.originType=='bk'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='app'&&icc.profileImageUrl==null || icc.originType=='app'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='zw'&&icc.profileImageUrl==null || icc.originType=='zw'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='baokan'&&icc.profileImageUrl==null || icc.originType=='baokan'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='jw'&&icc.profileImageUrl==null || icc.originType=='jw'&&icc.profileImageUrl=='' -->
							    <!-- ngIf: icc.originType=='wz'&&icc.profileImageUrl==null || icc.originType=='wz'&&icc.profileImageUrl=='' -->

								<span class="user-level-icon-wrapper">
							     <!-- ngIf: icc.verifiedType == 600 -->
							     <!-- ngIf: icc.verifiedType == 200 || icc.verifiedType == 220 -->
							     <!-- ngIf: icc.verifiedType == 1 || icc.verifiedType == 2 || icc.verifiedType == 3 || icc.verifiedType == 4 || icc.verifiedType == 5 || icc.verifiedType == 6 || icc.verifiedType == 7 -->
									<!-- <i class="user-level-icon weibo-gray"></i>
                                    <i class="user-level-icon weibo-pink"></i> -->
							     <!-- ngIf: icc.verifiedType == 0 -->
							 </span>
							</div>
						</div>

						<div class="inline-block news-item ddd">
							<div class="profile-title inline-block">
								<!-- 标题或者作者 start -->
								<!-- ngIf: icc.originType=='wb'&& icc.captureWebsiteName=='微博头条' -->
								<!-- ngIf: icc.originType=='wb'&&icc.author=='' && icc.captureWebsiteName!='微博头条' -->
								<!-- ngIf: icc.originType=='wb'&&icc.author!=''&&icc.author!=null && icc.captureWebsiteName!='微博头条' -->
								<!-- ngIf: icc.originType=='wx' -->
								
								<!-- ngIf: icc.originType!='wb' && icc.originType!='wx' --><a href="" value="316214740215654652355411" ng-click="getDetail(icc,currentKeyword);" ng-if="icc.originType!='wb' &amp;&amp; icc.originType!='wx'" class="ng-scope">
								   <!-- ngIf: (icc.originType=='app' || icc.originType=='lt') && icc.author!=''&&icc.author!=null -->
								   <span ng-bind-html="icc.title | trustAsHtml" class="ng-binding">没拿到救命钱，又一家快递公司破产，团队规模曾达8万人</span>
								</a><!-- end ngIf: icc.originType!='wb' && icc.originType!='wx' -->
								<!-- ngIf: icc.originType=='sp'&&icc.title=='' && icc.author!='' -->
								<!-- 标题或者作者 end -->

								<!-- 标属性 start -->
								<div class="inline-block select-wrapper bar-select" ng-show="view.resultPresent != 3">
									<div class="sensitive-status-wrapper p-r">
                                        <div class="sensitive-status-content mg ng-hide" data-toggle="dropdown" ng-show="icc.customFlag1 == 1 || icc.customFlag1 == 2 || icc.customFlag1 == 3">
                                            <span class="inline-block">敏感</span>
                                            <span class="inline-block fa"></span>
                                        </div>
                                        <div class="sensitive-status-content fmg ng-hide" data-toggle="dropdown" ng-show="icc.customFlag1 == 4">
                                            <span class="inline-block">非敏感</span>
                                            <span class="inline-block fa"></span>
                                        </div>
                                        <div class="sensitive-status-content zx" data-toggle="dropdown" ng-show="icc.customFlag1 == 5">
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
							<!-- 内容 start -->
							<div class="item-title news-item-title contenttext ng-binding" ng-bind-html="icc.summary | trustAsHtml">宅急送获10亿元B轮融资、<font color="red">安能物流</font>踏上赴港上市之路......一些二线快递企业在资本市场传出了利好，但这究竟是二线快递的新生，还是它们最后的倔强？缝隙市场能够容纳多少二线企业？</div>

							<!-- 内容 end -->
							<!-- 图片 start -->
							<!-- ngIf: icc.images!=null -->
							<!-- 图片 end -->

							<!-- 微博转发内容 start-->
							<!-- ngIf: icc.forwarderContent!='' && icc.forwarderContent!=null -->
							<!-- 微博转发内容 end-->

							
								
									
									
								
							

							 <!-- ngIf: icc.captureWebsiteName=="新浪微博" || icc.originType=="wb" || icc.captureWebsiteName=="腾讯微博" -->

							<div class="news-item-tools font-size-0">
								<div class="inline-block vertical-align-middle" style="width: calc(100% - 320px);">
									<!-- ngIf: icc.captureWebsiteName=="新浪微博" || icc.originType=="wb" || icc.captureWebsiteName=="腾讯微博" -->
									<!-- ngIf: icc.weiboHandleType==3 -->
									<div class="inline-block mr5">
										<span class="tippy font-size-16 vertical-align-middle color-gray" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" data-tippy="" data-original-title="涉及行业"><i class="fa"></i></span>
										<span class=" font-size-12 vertical-align-middle color-gray">
											<!-- ngRepeat: secondTrade in icc.secondTradeList --><!-- ngIf: secondTrade!=null --><div class="inline-block vertical-align-middle mr5 ng-binding ng-scope" ng-repeat="secondTrade in icc.secondTradeList" ng-if="secondTrade!=null">其他</div><!-- end ngIf: secondTrade!=null --><!-- end ngRepeat: secondTrade in icc.secondTradeList -->
											<!-- ngRepeat: thirdTrade in icc.thirdTradeList --><!-- ngIf: secondTrade!=null --><!-- end ngRepeat: thirdTrade in icc.thirdTradeList -->
		  								</span>
									</div>
									<div class="inline-block mr10">
										<span class="tippy font-size-16 vertical-align-middle color-gray" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" data-tippy="" data-original-title="精准地域"><i class="fa"></i></span>
										<span class=" font-size-12 vertical-align-middle color-gray">
											<div class="inline-block vertical-align-middle ng-binding" style="color: #2A5585;" ng-bind="icc.contentAddress">广东省,东莞市,深圳市</div>
		  								</span>
									</div>
									<div class="inline-block relative-keyword">
										<span class="tippy font-size-16 vertical-align-middle color-gray" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" data-tippy="" data-original-title="涉及词"><i class="fa"></i></span>
										<span class="font-size-12 vertical-align-middle  ng-binding" style="color: #FF0000;" ng-bind="icc.referenceKeyword">安能物流</span>
									</div>
									
								</div>

								<div class="inline-block news-item-tools text-right vertical-align-middle" style="width: 320px;">
									<div class="btn-group inline-block" role="group">
										<ul class="font-size-0">
										 <!-- 先写死，后期可控制 -->
										
											<li class="inline-block  dropdown" ng-class="{'dropdown':icclist.length != $index+1,'dropup':icclist.length == $index+1}" ng-show="view.resultPresent != 3">
												<!-- ngIf: icclist.length != $index+1 --><button ng-if="icclist.length != $index+1" type="button" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" class="tippy btn btn-default-icon fa-collection dropdown-toggle ng-scope" id="scj_316214740215654652355411" data-tippy="" data-original-title="添加至收藏夹">
												</button><!-- end ngIf: icclist.length != $index+1 -->
												<!-- ngIf: icclist.length == $index+1 -->
												<!-- ngIf: collectFoldersList!=null&&collectFoldersList.length>0 --><ul class="dropdown-menu ng-scope" role="menu" ng-if="collectFoldersList!=null&amp;&amp;collectFoldersList.length>0">
													<!-- ngRepeat: collect in collectFoldersList --><!-- ngIf: collect!=null --><li role="presentation" ng-repeat="collect in collectFoldersList" ng-if="collect!=null" class="ng-scope">
														<a href="javascript:void(0)" role="menuitem" ng-click="insertMaterial(collect.folderId,1,icc)"> <!--<span class="icon fa-user"></span>-->
															<span class="fa-key ng-binding" ng-bind="collect.name">默认收藏夹</span>
														</a>
													</li><!-- end ngIf: collect!=null --><!-- end ngRepeat: collect in collectFoldersList -->
												</ul><!-- end ngIf: collectFoldersList!=null&&collectFoldersList.length>0 -->
											</li>
											<li class="inline-block  dropdown" ng-class="{'dropdown':icclist.length != $index+1,'dropup':icclist.length == $index+1}" ng-show="view.resultPresent != 3">
												<!-- ngIf: icclist.length != $index+1 --><button ng-if="icclist.length != $index+1" type="button" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" class="tippy btn btn-default-icon fa-news-material dropdown-toggle ng-scope" id="sck_316214740215654652355411" data-tippy="" data-original-title="添加至简报素材">
												</button><!-- end ngIf: icclist.length != $index+1 -->
												<!-- ngIf: icclist.length == $index+1 -->
												<!-- ngIf: briefFoldersList!=null&&briefFoldersList.length>0 --><ul class="dropdown-menu ng-scope" role="menu" ng-if="briefFoldersList!=null&amp;&amp;briefFoldersList.length>0">
													<!-- ngRepeat: brief in briefFoldersList --><!-- ngIf: brief!=null --><li role="presentation" ng-repeat="brief in briefFoldersList" ng-if="brief!=null" class="ng-scope">
														<a href="javascript:void(0)" role="menuitem" ng-click="insertMaterial(brief.folderId,2,icc)"> <!--<span class="icon fa-user"></span>-->
															<span class="fa-key ng-binding" ng-bind="brief.name">默认素材库</span>
														</a>
													</li><!-- end ngIf: brief!=null --><!-- end ngRepeat: brief in briefFoldersList -->
												</ul><!-- end ngIf: briefFoldersList!=null&&briefFoldersList.length>0 -->
											</li>
										

											<li class="inline-block dropdown" ng-class="{'dropdown':icclist.length != $index+1,'dropup':icclist.length == $index+1}" ng-show="view.resultPresent != 3">
												<!-- ngIf: icclist.length != $index+1 --><button ng-if="icclist.length != $index+1" type="button" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" class="tippy btn btn-default-icon fa-send-way dropdown-toggle ng-scope" data-tippy="" data-original-title="舆情下发渠道"></button><!-- end ngIf: icclist.length != $index+1 -->
												<!-- ngIf: icclist.length == $index+1 -->
												<ul class="dropdown-menu pt15 pb15" role="menu">
													
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="getAddressBook(2,icc,1);">
															<span class="fa-key">短信下发</span>
														</a>
													</li>
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="getAddressBook(1,icc,1);">
															<span class="fa-key">邮件下发</span>
														</a>
													</li>
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="getAddressBook(3,icc,1);">
															<span class="fa-key">微信下发</span>
														</a>
													</li>
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="shareQQ(icc)">
															<span class="fa-key">QQ下发</span>
														</a>
													</li>
													
													
												</ul>
											</li>
											<li class="inline-block">
												<a href="https://page.om.qq.com/page/ONGT2PT2KiRMnc_BgWfVJS_A0" target="_blank" class="">
                                                <button type="button" data-tippy-placement="top" aria-expanded="false" class="tippy btn btn-default-icon fa-check-origin-link" data-tippy="" data-original-title="查看原文"></button>
                                                </a>
											</li>
											<li class="inline-block dropdown">
												
												<button type="button" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" class="tippy btn btn-default-icon fa-copy-direct dropdown-toggle" data-tippy="" data-original-title="复制">
												</button>
												<ul class="dropdown-menu" role="menu">
													<li role="presentation">
														<a href="javascript:void(0)" id="link_316214740215654652355411" role="menuitem" ng-click="copyLink(icc.webpageUrl,icc.id);">
															
															<span class="fa-key">拷贝地址</span>
														</a>
													</li>
													<li role="presentation">
														<a href="javascript:void(0)" class="copy-link-custom" role="menuitem" ng-click="aKeyToCopy(icc);">
															<span class="fa-key">一键复制</span>
														</a>
													</li>
												</ul>
											</li>
											<li class="inline-block" ng-show="icc.readFlag==undefined &amp;&amp; view.resultPresent != 3">
												<button type="button" data-tippy-placement="top" class="tippy btn btn-default-icon fa-unread-status" ng-click="readNews($event,icc)" data-tippy="" data-original-title="标已读"> </button>
											</li>
											<li class="inline-block ng-hide" ng-show="icc.readFlag=='1' &amp;&amp; view.resultPresent != 3">
												<button type="button" data-tippy-placement="top" class="tippy btn btn-default-icon fa-read-status waves-effect waves-light color-blue" data-tippy="" data-original-title="已读">
												</button>
											</li>
                                            







                                         
											<li class="inline-block" ng-show="view.resultPresent != 3">
												<button type="button" data-tippy-placement="top" data-hover="dropdown" data-toggle="dropdown" data-animation="scale-up" data-delay="300" aria-expanded="false" class="tippy btn btn-default-icon fa-trash dropdown-toggle" data-tippy="" data-original-title="删除">
												</button>
												<ul class="dropdown-menu" role="menu" style="margin-left: 88%;">
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="deleteSolrIds(icc)">
															<span class="fa-key">删除信息</span>
														</a>
													</li>
													<li role="presentation">
														<a href="javascript:void(0)" role="menuitem" ng-click="excludeCaptureWebsiteNameList(icc)">
															<span class="fa-key">删除信息并排除来源</span>
														</a>
													</li>
													
												</ul>
											</li>
											
											<li class="inline-block ng-hide" ng-show="icc.originType=='wb' &amp;&amp; icc.captureWebsiteName=='新浪微博' &amp;&amp; view.resultPresent != 3">
													<button type="button" data-tippy-placement="top" class="tippy btn btn-default-icon fa-suyuan" data-toggle="modal" ng-click="oneKeyTracingDetail(icc)" data-tippy="" data-original-title="信息溯源">
                                         		</button>
                                        	</li>
                                        	<li class="inline-block" ng-show="icc.originType=='xw' &amp;&amp; view.resultPresent != 3">
													<button type="button" data-tippy-placement="top" class="tippy btn btn-default-icon fa-suyuan" data-toggle="modal" ng-click="oneKeyTracingXwDetail(icc)" data-tippy="" data-original-title="信息溯源">
                                         		</button>
                                        	</li>
											
										</ul>
									</div>
								</div>
							</div>
						</div>
					</div>
				</td>
"""
from pyquery import PyQuery as pq
doc=pq(tdtitle)
print(doc.find('div[ng-bind="icc.contentAddress"]').text())