import asyncio
import json
import re
import time

from log import logger

import aiohttp

params = {
    "area_Id": 10099,
    "groupId": 10035,
    "qry_no": "1________06",
    "page_num": 1
}

are_code = {
    "尖山区": 10099,
    "集贤县": 10100,
    "宝清县": 10101,
    "饶河县": 10102,
    "友谊县": 10103,
    "宝山区": 198623
}

cite_code = {
    "双鸭山": 10035
}

task_code = [
    # "00",
    # "11",
    # "06",
    # "41",
    # "42",
    # "46",
    # "49",
    # "64",
    # "74",
    # "53",
    # "55",
    # "58",
    "63",
    # "68",
    "87",
    "93",
    # "98"
]


async def get_dianxin(params, city):
    async with aiohttp.ClientSession() as session:
        for search_value in task_code:
            with open("./result/移动result.txt", 'a+') as file_object:
                params['qry_no'] = params['qry_no'][0:-2] + search_value
                print(len(params['qry_no']))
                for area in are_code.values():
                    params['area_Id'] = area
                    for idx in range(1, 200):
                        params['page_num'] = idx
                        async with session.get('http://www.hl.10086.cn/rest/webchoose/qryNormalNoList',
                                                params=params) as resp:
                            r = await resp.json()
                            try:
                                num_list = [str(x['PHONE_NO']) for x in r['data']['PHONE_LIST'] if
                                            x['PHONE_NO'][-2:] == search_value]
                                if not num_list:
                                    logger.info("no search_number:{0}".format(search_value))
                                    continue
                                str_list = "，\n".join(num_list)
                                a_line = "，\n{0}".format(str_list)
                                file_object.write(a_line)
                                logger.info("done search_number:{0}".format(search_value))
                            except Exception as e:
                                logger.info(r['retMsg'])
                                break

        print("爬取任务已完成")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_dianxin(params, "双鸭山"))
    loop.close()
