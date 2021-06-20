import requests
from bs4 import BeautifulSoup

companys = {
    "移动": 19,
    "联通": 20
}

citys = {
    "杭州": 1101
}

codes = [
    '11', '00', '53', '93', '55', '58', '06', '46', '64', '68', '49', '98'
]


def get_taohao(company, city):
    with open("./result/taohao_result.txt", 'a+') as file_object:
        ccompany = companys[company]
        ccity = citys[city]
        # for task_code in codes:
        for task_code in codes:
            page_p = 0
            last_number = ''
            while True:
                try:
                    page_p += 1
                    url_ = f'http://t.9taohao.com/product/default.aspx?company={ccompany}&city={ccity}&type=mb&keyword=1________{task_code}'
                    if page_p >= 2:
                        url_ += f'&page={page_p}'
                    resp = requests.get(url_)
                    soup = BeautifulSoup(resp.content, 'html.parser')
                    mobiles = [li.text for li in soup.find_all('li', class_='li_mobile')]
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
