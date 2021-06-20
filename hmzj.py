import asyncio
import json
import re
import time

from log import logger

import aiohttp

headers = {
    "Referer": "http://sz.haoma.com/xh/?dis=8"
}

params = {
    "cnt": 500,
    "page_no": 1,
    "numcategory": 0,
    "dis": 8,
    "lanmu": 2,
    "klist": '1__________',
    "st": 4
}

cite_code = {
    "珠海": 8,
    "广州": 1,
    "昆明": 1,
    '深圳': 6,
    '成都': 1,
}

company_code = {
    '联通': 1,
    '电信': 2,
    '移动': 0
}

task_code = [
    '11', '06', '41', '42', '46', '49', '64', '74', '58', '28', '68', '87', '98',
]

urls = {
    "广州": "http://gd.haoma.com/io/5.asp",
    "珠海": "http://sz.haoma.com/io/5.asp",
    "昆明": "http://yn.haoma.com/io/5.asp",
    "深圳": "http://sz.haoma.com/io/5.asp",
    "成都": "http://cd.haoma.com/io/5.asp"
}


async def get_dianxin(params, city, company):
    url = urls[city]
    params['dis'] = cite_code[city]
    # params['lanmu'] = company_code[company]
    async with aiohttp.ClientSession() as session:
        # for search_value in task_code:
            # params['klist'] = '1________{}'.format(search_value)
            with open("./result/号码之家result.txt", 'a+') as file_object:
                for idx in range(1, 181):
                    params['page_no'] = idx
                    async with session.get(url,
                                           params=params, headers=headers) as resp:
                        r = await resp.text()
                        print(resp.url,r)
                        try:
                            num_list = []
                            values_1 = r.split('|')
                            for value_2 in values_1:
                                num_value = value_2.split(',')
                                if not num_value or len(num_value) < 3:
                                    continue
                                num_list.append(num_value[0])
                            str_list = "，\n".join(num_list)
                            a_line = "，\n{0}".format(str_list)
                            file_object.write(a_line)
                            # logger.info("done search_number:{}".format(search_value))
                        except Exception as e:
                            logger.info(e)
                            logger.info(r)
                            break

    print("爬取任务已完成")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_dianxin(params, "成都", "联通"))
    loop.close()
