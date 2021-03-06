#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/23 11:16
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 表情过滤3.py
 Description:
 Software   : PyCharm
"""
import re
def emoji_filter(desstr, restr=''):
    co = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])|"  # flags (iOS)
        u"(…)|"
        u'(#)|'
        u'(❤)|'
        u'(\ud83e[\udde0-\uddff])|'
        u'([\U00010000-\U0010ffff])|'
        u'([\uD800-\uDBFF][\uDC00-\uDFFF])|'
        u'(@)', flags=re.UNICODE)

    return co.sub(restr, desstr)

test_str="""
(5718494661388618752, 11, "以有lg/❤:@🌺婷婷🍀很乖 😘(O1233354969) @温柔宏 /🎱(O1056970499) @我们散开吧!(O1663851080)
 @汤利🐸(O909028664) @黑白呢.......(O1439228824) @好想打阔睡(O2030413174) @苏冉⊙∀⊙!(O1250956323) @❤️
 乖乖女$珍宝❤️(O2433072046) @小可可爱❤️❤️❤️❤️(O1151763270) @阿燕(互粉)(O2296597437) 
 @❤熊和兔(O1107485951) @不如放弃✨(O2416618973) @可爱宝宝0026(O2481201559) @卡丁车(O2362036833) 
 @💞琳妹💞(O2283113451) @非正常人!(O2350172214) @閃友的酒(O1020071942) @卑微的小学(O1679105667) 
 @文庭(O2207423839) @烟起雾散(冲1000)(O2064821100) @奶泡星球.com🤗(O1811179098) @倩💓豆💓豆(O1468588301) 
 @ᝰꫛꫀꪝ言52o1⁄31⁄4🕊(O1080037300) @🕊️抑郁~女孩💔(O1590924264) @~依旧✔张无道卍(O546350713) @月野_🍒兔(O1278165188) 
 @济宁農村人我(O1278408075) @阿。🌴·伟(O1278487390) @算明💕(O1908720897) @❤苗族🍃阿平✨(O1985470472) 
 @镇海\n优速\n物流(O800166092) @T_TGG(O2439891110) @香(O2467894391) @深情续以晚霞ʚɞ(O1753525562) 
 @徐..🀄平..🎱(O2388858086) @悠悠🍀安静🌈(O1309186174) @家有公主(倚后)(O1215999789) @1⃣琴.....(O2205243374)
  @苏皖洛(O2212064203) @阿 ―总(O1266272518) @苗族男孩一一🙈DJ乖乖(O1798859525) @💕对霞的温柔💕(O2391769117) 
  @胜华✨☀️学长(O1449753675) @云南:TM(O1739573051) @爱这❌苗家人⭕🅰(O2413052798) @Maked(O2258964441) 
  @對你,何止1.句喜歡!(O1339782654) @和平精英---多多(O1772427448) @港島日人覺(O1278253601) @佛袖~(O1278162058) 
  @朝阳c.(O1278420597) @💕洗美不爱💕(O1793062526) @没人爱的渣男只有游戏爱(O2115493150) @❤️宠🌺陆🌸风❤️
  (O2282753145) @我要乖1⃣️点啦❤️(O1790077190) @赵兴林(O1881161377) @伊伊宝❤️🕊(O1338275118) @《嫉妒💔》
  俊(O1454001122) @Thea(O2372420196) @我不搞伤感💞只搞精神(O2446708812) @帅哥 😜😜(O2190380476) @依依💔💔(O2402238056) 
  @语轩🍎(O2364752869) @qr一🍃🍃🍃🍃(O2374040274) @风淡云轻(O2452202882) @“最后的深情”(O2204156653) @暗示.👻(O2205292421) 
  @如直接(O2421645421) @颜心心(O2466144200) @🍒苗族🍒咪哆蒙🍒(O2389142585) @✺(^O^)✺小米🍀(O573762769) @仙衣-和平精英(O304397196)
   @YANG.春麗(O2323521055) @梅宝🌺🌺(O1981246735) @小珍珠二宝(O1278129484) @-Saku☃rakoˇ(O2293744346) @txy💞(O2003543544) 
   @☞莫问归期冲3000(O1429208899) @🌴橙汁🌴(O2353949954) @错~季 *(O636496059) @小李与小唐(O1098895934) 
   @请叫我夕阳OK(O214@陪江哥长大(O1953247678) @张春成,,(O1064454048) @遥遥江上客💞(O2090360388) @❀瞅.(O2434822172) 
   @一笑吖ღ ͜✿҉(O107604674) @卿......🌊(O2442145722) @一路精神(O2238181564) @爱56453(O1637864027) 
   @ლ—(°◡°)-ლ😁(O1998262508) @小段......加油(●'◡'●)(O2445708482)", '伟(O1278487390) @算明💕(O1908720897) 
   @❤苗族🍃阿平✨(O1985470472) @镇海\n优速\n物流(O800166092) @T_TGG(O2439891110) @香(O2467894391) @深情续以晚霞', 
   '<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;white-space: -pre-wrap;white-space: -o-pre-wrap; 
   word-wrap: break-word;"><zhengwen>@婷婷很乖 (O1233354969) @温柔宏 /(O1056970499) @我们散开吧！(O1663851080) 
   @汤利(O909028664) @黑白呢.......(O1439228824) @好想打阔睡(O2030413174) @苏冉⊙∀⊙！(O1250956323) 
   @❤️乖乖女$珍宝❤️(O2433072046) @小可可爱❤️❤️❤️❤️(O1151763270) @阿燕（互粉）(O2296597437) 
   @❤熊和兔(O1107485951) @不如放弃✨(O2416618973) @可爱宝宝0026(O2481201559) @卡丁车(O2362036833) @琳妹(O2283113451)
    @非正常人！(O2350172214) @閃友的酒(O1020071942) @卑微的小学(O1679105667) @文庭(O2207423839) @烟起雾散（冲1000）
    (O2064821100) @奶泡星球.com\ud83e\udd17(O1811179098) @倩豆豆(O1468588301) @ᝰꫛꫀꪝ言⁵²º⅓¼(O1080037300) @️
    抑郁～女孩(O1590924264) @～依旧✔张无道卍(O546350713)  @月野︴兔(O1278165188)  @济宁農村人我(O1278408075) 
    @阿。·伟(O1278487390) @算明(O1908720897) @❤苗族阿平✨(O1985470472) @镇海<font color="red">优速</font>
    物流(O800166092) @T_TGG(O2439891110) @香(O2467894391) @深情续以晚霞ʚɞ(O1753525562) @徐..\ud83c\udc04平..
    (O2388858086) @悠悠安静(O1309186174) @家有公主（倚后）(O1215999789) @1⃣琴.....(O2205243374) 
    @苏皖洛(O2212064203) @阿 ―总(O1266272518) @苗族男孩一一DJ乖乖(O1798859525)  @对霞的温柔(O2391769117) 
    @胜华✨☀️学长(O1449753675) @云南:™(O1739573051) @爱这❌苗家人⭕\ud83c\udd70(O2413052798) 
    @Maked(O2258964441) @對你,何止1.句喜歡！(O1339782654) @和平精英---多多(O1772427448) @港島日人覺(O1278253601) 
    @佛袖~(O1278162058) @朝阳c.(O1278420597) @洗美不爱(O1793062526) @没人爱的渣男只有游戏爱(O2115493150) @❤️宠陆风❤️
    (O2282753145) @我要乖1⃣️点啦❤️(O1790077190) @赵兴林(O1881161377) @伊伊宝❤️(O1338275118) @《嫉妒》俊(O1454001122)
     @Thea(O2372420196) @我不搞伤感只搞精神(O2446708812) @帅哥 (O2190380476) @依依(O2402238056) @语轩(O2364752869) 
     @qr一(O2374040274) @风淡云轻(O2452202882) @“最后的深情”(O2204156653)  @暗示.(O2205292421) @如直接(O2421645421) 
     @颜心心(O2466144200) @苗族咪哆蒙(O2389142585) @✺（^O^）✺小米(O573762769) @仙衣-和平精英(O304397196) 
     @YANG.春麗(O2323521055) @梅宝(O1981246735) @小珍珠二宝(O1278129484) @-Saku☃rakoˇ(O2293744346) @txy(O2003543544) @☞莫问归期冲3000(O1429208899) @橙汁(O2353949954) @错~季 *(O636496059) @小李与小唐(O1098895934) @请叫我夕阳OK(O214@陪江哥长大(O1953247678) @张春成，，(O1064454048) @遥遥江上客(O2090360388) @❀瞅.(O2434822172) @一笑吖ღ ͜✿҉(O107604674) @卿……(O2442145722) @一路精神(O2238181564) @爱56453(O1637864027) @ლ—（°◡°）-ლ(O1998262508) @小段……加油（●＇◡＇●）(O2445708482)</zhengwen></pre>', 'https://live.kuaishou.com/u/3xmmm4fkyqs6766/3xdhd8fcph63frq', '以有lg/❤', '2021-08-21 16:24', 2, '北京', 0.9)
"""
print(emoji_filter(test_str))