import math
import time
import sys
from json import loads, dumps
import requests
from my_fake_useragent import UserAgent as ua
import pandas as pd
import numpy as np
sys.path.append("D:\pythonEdit\Intelligent\scrapy_study\scrapy_student\\")
from prettytable import PrettyTable


def format_msg_table(data_list: list):
    """
    Z 需要 20：31 G需要 20：30 T需要20：31 D需要 20：30 K需要20：31  提取规则是 先最后四个，然后前面两个，然后不断先从后再从前拿一个, 返回的列表信息转换为严格的表格模式
    :param data_list:
    :return:
    """
    format_table_data = []
    for data in data_list:
        data = data.split("|")[3:]
        train_number, start_station_code, end_station_code, souce_station_code, dst_station_code, depart_time, arrive_time, experience_time = data[:8]
        analysis_list = data[20:30]
        if train_number[0].upper() in ["K", "T", "Z"]:
            analysis_list = data[20:31]
            # print(f"{train_number}按照20：31分析")
        # else:
            # print((f"{train_number}按照20：30分析"))
        last_four = [analysis_list[-i] for i in range(1, 5)]  # 从后往前依次取四个
        first_two = analysis_list[:2]  # 从前往后依次取两个
        trace_data = analysis_list[2:-4]
        last_four.extend(first_two)
        for i in range(math.ceil(len(trace_data) / 2)):  # 从后面开始，不断一后一前取数据
            last_four.append(trace_data[-(i + 1)])
            last_four.append(trace_data[i])
        if len(last_four) > 10:
            last_four = last_four[:10]  # 前面取数据时会有 其他 项造成不同，故只取到十个数据，即从商务座到无座，详情对照查询界面
        format_row_data = data[:8]
        format_row_data.extend(last_four)
        format_table_data.append(format_row_data)
    return format_table_data


# # 获取省份简称，用于以下搜索--原始数据收集
# province_name_url = 'https://www.12306.cn/index/script/core/common/station_name_v10151.js'
# province_request = requests.request(method="GET", url=province_name_url, headers={"User-Agent": ua().random()})
# json_data = province_request.text
# province_data = json_data.split("=")[-1].split('|')
# with open("./station_name.json", mode="w", errors="ignore") as f:
#     f.write(dumps({"data": province_data}))
# province_request.close()
# query_request.close()

def query_data_from_12306(departure_date: str, source_province_name: str, dst_province_name: str):
    # 加载车站停靠站名字文件
    with open("./station_name.json", mode="r", errors="ignore") as station_name_reader:
        province_data = loads(station_name_reader.read()).get("data")
    province_code = lambda x: province_data[province_data.index(x) + 1]
    province_name = lambda x: province_data[province_data.index(x) - 1]

    # 获取车站编号
    source_province_code = province_code(source_province_name)
    dst_province_code = province_code(dst_province_name)

    # 构造GET请求头
    query_url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={Departure_date}&leftTicketDTO.from_station={source_province_code}&leftTicketDTO.to_station={dst_province_code}&purpose_codes=ADULT"
    query_header = {
        "User-Agent": ua().random(),
        "Cookie": "JSESSIONID=7D918C4D866778BF475E2CEAB1D265C0; BIGipServerotn=1324352010.24610.0000; BIGipServerpool_passport=98828810.50215.0000; RAIL_EXPIRATION=1637364024492; RAIL_DEVICEID=CTVLmN9dhQp1IAXM0XyCfimTvUiwe5ZyT2NYNg6Ml9WnQCeqBdSzSedAlYiGhqRBdeZBc-BEytyiu2jSZc8BCGjhsP8PxPmGFz2wky_Mk5iuTni8K_ElaVcWN3g0TAx3wpkiQ5LiY8itYc2Of8r1b1Gu_TL2IHQV; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=9036359bb8a8a461c164a04f8f50b252"
    }
    session = requests.Session()

    # 请求数据
    query_request = session.get(url=query_url, allow_redirects=True, headers=query_header)
    msg_dict = loads(query_request.text)
    msg_list = msg_dict.get("data").get("result")
    query_request.close()

    # 将数据规则化，并可视化输出
    msg_datas = format_msg_table(data_list=msg_list)
    query_result = []
    for msg_data in msg_datas:
        station_name = [province_name(station_code) for station_code in msg_data[1:5]]
        msg = [msg_data[0]] + station_name + msg_data[5:]
        query_result.append(msg)

    # 信息展示

    # 采用pandas进行展示
    # query_show_data = pd.DataFrame(query_result)
    # query_show_data.columns = ["列车车次", "起始站", "终点站", "乘车始站", "乘车末站", "出发时间", "预计到达时间", "历时", "商务座\特等座",
                        # "一等座", "二等座", "高级软卧", "一等卧（软卧）", "动卧", "硬卧（二等卧）", "软座", "硬座", "无座"]
    # query_show_data[query_show_data == ""] = np.nan
    # query_show_data.to_excel('./temp.xlsx')  # 将结果保存到本地或者指定的地方进行缓存

    #  直接输出展示
    show_table = PrettyTable()
    show_table.field_names = ["列车车次", "起始站", "终点站", "乘车始站", "乘车末站", "出发时间", "预计到达时间", "历时",
                              "商务座\特等座","一等座", "二等座", "高级软卧", "一等卧（软卧）", "动卧", "硬卧（二等卧）", "软座",
                              "硬座", "无座"]
    for row in query_result:
        show_table.add_row(row=[i if i else "-" for i in row])
    show_table.align = "c"
    show_table.valign = "m"
    print(show_table)
#
if __name__ == '__main__':
    # 查询日期的车次信息
    Departure_date = "2021-11-19"
    source_province_name = "杭州南"
    dst_province_name = "苏州"
    query_data_from_12306(departure_date=Departure_date, source_province_name=source_province_name, dst_province_name=dst_province_name)
# province_request.close()