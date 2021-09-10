k_list=['爱色丽彩通', 'X-rite Pantone', '德塔颜色', 'Datacolor', '毕克铜陵', 'BYK-Gardner', '亨特立 ', 'Hunterlab', '三恩驰', ' 3nh', '杭州彩谱', 'China Spec', '远方光电', 'Everfine', '精测电子 ', 'Jingce']
str_2="56+5+三恩驰"
def test():
    for item in k_list:
        if item in str_2:
            return True
    return False

print(test())

