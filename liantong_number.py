import asyncio
import re

from log import logger

import aiohttp

params = {
    "callback": "jsonp_queryMoreNums",
    "provinceCode": 97,
    "cityCode": 994,
    "monthFeeLimit": 0,
    "groupKey": 4200332935,
    "net": "01",
    "searchCategory": 3,
    "codeTypeCode": "",
    "advancePayLower": 0,
    "searchValue": "",
    "qryType": "02",
    "goodsNet": 4,
    "_": ""
}

card_dict = {
    # 4200332935: "黑龙江39元流量王",
    # 9301858665: "【生日号】黑龙江39元流量王;",
    # 4201858666: "【钻石号】黑龙江39元流量王;",
    # 9901858662: "【爱情号】黑龙江39元流量王;",
    # 49236584: "腾讯王卡-地王卡;阿里小宝卡（新）;",
    # 3901858663: "【发达号】黑龙江39元流量王;",
    # 2702314874: "AAA靓号】5G畅爽冰激凌-199档;",
    # 8401859252: "学霸号】黑龙江39元流量王;",
    # 7401858667: "红色号】黑龙江39元流量王;",
    # 5100255964: "5G畅爽冰激凌-159 AABB ABAB靓号;",

    # 36243047: "山东济南腾讯地王卡",
    # 17236695: "山东济南腾讯天王卡",
    # 3100271134: "山东济南冰激凌",
    # 85236889: "北京腾讯地王",
    # 2802294079: "全国流量王",

    4700248566: "大王卡,冰激凌",
    5202291606: "钉钉小宝",
    6902238226: "珠海aaa大王卡",
    7300295357: "珠海帆船",
    40210219: "珠海发达",
    5700291031: "珠海新号",
    73044235: "珠海米粉卡",
    79147959: "珠海生日",
    44203796: "珠海爱情",
    89162743: "珠海吉祥",
    1000287829: "珠海学霸",

    # 90242110: "新疆大王卡",
    # 43236612: "甘肃大王卡",
    # 20236750: "王卡"

    # 杭州
    # 5300580856:"大王卡",
    # 362004075943:"幸福卡",
    # 湖南
    # 72097646: "长沙流量王",
    # 6201612108: "王卡鸿运",
    # 1701612110: "xb鸿运",
    # 9201612109: "jn鸿运",
    # 9201612106: "aq鸿运",
    # 742004086051: "diwang",

    # 云南
    # 1900289281: "王卡",

    # 山西
    # 8500303192: "王卡",

    # 南昌
    # 35228836: "王卡",

}

province_code = {
    "新疆": 89,
    "广东": 51,
    "黑龙江": 97,
    "山东": 17,
    "北京": 11,
    "内蒙古": 10,
    "云南": 86,
    "甘肃": 87,
    "四川": 81,
    "浙江": 36,
    "湖南": 74,
    "山西": 19,
    "江西": 75
}

cite_code = {
    "南昌": 750,
    "长沙": 741,
    "株洲": 742,
    "杭州": 360,
    "成都": 810,
    "中山": 556,
    "珠海": 620,
    "白银": 879,
    "乌鲁木齐": 890,
    "广州": 510,
    "昆明": 860,
    "红河": 861,
    "哈尔滨": 971,
    "齐齐哈尔": 973,
    "牡丹江": 988,
    "佳木斯": 976,
    "绥化": 989,
    "大庆": 981,
    "鸡西": 991,
    "黑河": 990,
    "双鸭山": 994,
    "鹤岗": 993,
    "七台河": 992,
    "大兴安岭": 995,
    "济南": 170,
    "北京": 110,
    "呼伦贝尔": 108,
    "西双版纳": 736,
    "太原": 190,
}

task_code = [
    '68','28','42','06','41','46','49','64','74','11',
]


async def get_liantong(params, province, city):
    async with aiohttp.ClientSession() as session:
        check_list = []
        with open("./result/联通result.txt", 'a+') as file_object:
            for search_value in task_code:
                for groupKey in card_dict.keys():
                    # file_object.write('\n\n{}\n\n'.format(card_dict[groupKey]))
                    params['groupKey'] = groupKey
                    params['provinceCode'] = province_code[province]
                    params['cityCode'] = cite_code[city]
                    params['searchValue'] = search_value
                    for i in range(20):
                        async with session.get('http://cd.10010.com/NumApp/NumberCenter/qryNum',
                                               params=params) as resp:
                            r = await resp.text()
                            print(r)
                            try:
                                r_ = re.findall(r'[(](.*?)[)]', r)
                                r_dict = eval(r_[0])
                                num_list_from = r_dict['numArray']
                                num_list = [i for i in num_list_from if len(str(i)) == 11]
                                if not num_list:
                                    print("no{0}".format(search_value))
                                    break

                                key_list = [str(x) for x in num_list if
                                            x not in check_list and str(x)[-2:] == search_value]
                                if key_list:
                                    str_list = "，\n".join(key_list)
                                    check_list.extend(num_list)
                                    check_list = list(set(check_list))

                                    a_line = "，\n{0}".format(str_list)
                                    file_object.write(a_line)
                                    print("done:{0}".format(search_value))
                            except Exception as e:
                                logger.info(e)
        print("爬取任务已完成")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_liantong(params, "广东", "珠海"))
    loop.close()
