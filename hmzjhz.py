import requests
from bs4 import BeautifulSoup

companys = {
    "移动": 'yd',
    "联通": 'lt'
}

citys = {
    "杭州": 3100000
}

codes = [
    '11', '00', '53', '93', '55', '58', '06', '46', '64', '68', '49', '98'
]


def get_taohao(company, city):
    with open("./result/hmzj_hz_result.txt", 'a+') as file_object:
        ccompany = companys[company]
        ccity = citys[city]
        # for task_code in codes:
        for task_code in codes:
            page_p = 0
            last_number = ''
            while True:
                try:
                    print(f"{task_code}:{page_p}")
                    page_p += 1
                    data = {
                        'ExactPosition': f'1????????{task_code}',
                        'pageSize': 50,
                        'coupleType': '000001',
                        'pageIndex': 1,
                        'city': ccity,
                        'type': '000001',
                        'operator': ccompany
                    }
                    url_ = f'https://api.haoma.cn/numberfront/numberfront/revert/queryList'
                    if page_p >= 2:
                        data['pageIndex'] = page_p
                    resp = requests.post(url_, data=data)
                    datas = resp.json()
                    mobiles = [mobile['number'] for mobile in datas['date']['list']]
                    if mobiles[-1] == last_number:
                        break
                    else:
                        last_number = mobiles[-1]
                    str_list = "，\n".join(mobiles)
                    a_line = "，\n{0}".format(str_list)
                    file_object.write(a_line)
                except Exception as e:
                    print(e)
                    break


if __name__ == '__main__':
    get_taohao('移动', '杭州')
