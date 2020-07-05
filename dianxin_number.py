import asyncio
import json
import re
import time

from log import logger

import aiohttp

params = {
    "method": "getPhoneInfo"
}

data = {
    "provincecode": 609910,
    "areacode": 8230500,
    "shopId": 10036,
    "salesProdId": "00000000A25E3D1B0CD272F4E053AC1410AC4D1B",
    "pageindex": 1,
    "pagesize": 3000,
    "submitType": 5,
    "contnumber": ""
}

province_code = {
    "黑龙江": 609910
}

cite_code = {
    "双鸭山": 8230500
}

task_code = [
    "00",
    "11",
    "06",
    "41",
    "42",
    "46",
    "49",
    "64",
    "74",
    "53",
    "55",
    "58",
    "68"
]


async def get_dianxin(params, data, province, city):
    async with aiohttp.ClientSession() as session:
        check_list = []
        for search_value in task_code:
            with open("./result/电信result.txt", 'a+') as file_object:
                data['provincecode'] = province_code[province]
                data['areacode'] = cite_code[city]
                data['contnumber'] = search_value
                async with session.post('http://www.189.cn/dqmh/seniorPhone/search.do',
                                        params=params, data=data) as resp:
                    r = await resp.json()
                    # maxidx = r[0]['maxPage'] if r[0]['maxPage'] < 5 else 5
                    num_list = [str(x['phoneNumber']) for x in r[0]['listphones'] if
                                x['phoneNumber'][-2:] == search_value]
                    if not num_list:
                        logger.info("no search_number:{0}".format(search_value))
                        continue
                    str_list = "，\n".join(num_list)
                    a_line = "，\n{0}".format(str_list)
                    file_object.write(a_line)
                    logger.info("done search_number:{0}".format(search_value))
                # for inx in range(2, maxidx + 1):
                #     data['pageindex'] = inx
                #     async with session.post('http://www.189.cn/dqmh/seniorPhone/search.do',
                #                             params=params, data=data) as resp:
                #         r = await resp.json()
                #         # logger.info(json.dumps(r))
                #         # a_line = "，\n{0}".format(str_list)
                #         num_list = [str(x['phoneNumber']) for x in r[0]['listphones'] if
                #                     x['phoneNumber'][-2:] == search_value]
                #         if not num_list:
                #             logger.info("no search_number:{0}".format(search_value))
                #             continue
                #         str_list = "，\n".join(num_list)
                #         a_line = "，\n{0}".format(str_list)
                #         file_object.write(a_line)
                #         logger.info("done search_number:{0}".format(search_value))
                        # time.sleep(10)
                        # print(r)

        print("爬取任务已完成")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_dianxin(params, data, "黑龙江", "双鸭山"))
    loop.close()
