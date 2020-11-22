import requests
from bs4 import BeautifulSoup

area_code = {
    "珠海": "200_756"
}
url = 'https://shop.10086.cn/list/134_{}_1_0_0_0_0_0.html'.format(area_code['珠海'])
number_list = []
for p in range(1, 50):
    number_list = []
    html_doc = requests.get(url, params={'p': p})
    # print(html_doc.content)
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    task_code = [
        '00',
        '11',
        '06',
        '28',
        '42',
        '41',
        '46',
        '49',
        '64',
        '74',
        '53',
        '55',
        '58',
        '87'
    ]

    for i in soup.find_all('td', class_='name'):
        num = i.text
        if num[-2:] in task_code:
            number_list.append(num)
            print(num)
    print(number_list)

    with open("./result/移动new_result.txt", 'a+') as file_object:
        str_list = "，\n".join(number_list)
        a_line = "，\n{0}".format(str_list)
        file_object.write(a_line)
