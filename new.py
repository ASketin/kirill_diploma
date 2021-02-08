import csv
import vk
import time
import numpy as np
import pandas as pd
from config import LOGIN, PASSWORD, ID, ACCESS_TOKEN
from vk_script import modify_script, get_friend_script


def write_data(source: str, year: int) -> None:
    parse = source.split(',')
    current_pos = 0
    end = 6
    with open(f'Nsk_{year}.csv', 'w', newline='', encoding='utf-8') as output:
        id_writer = csv.writer(output, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        while end < len(parse):
            id_writer.writerow(parse[current_pos:end])
            current_pos = end
            end = current_pos + 6
            if end >= len(parse):
                end = len(parse)


def mine_users(start_year: int, end_year: int, city_code: int) -> None:
    start = time.time()
    while start_year >= end_year:
        request = modify_script(city_code, start_year)
        data = api.execute(code=request, v="5.126")
        time.sleep(1)
        write_data(data, start_year)
        start_year -= 1
    print(time.time() - start)


def get_friends(db_path: str, output_name: str) -> None:
    start_time = time.time()
    data = pd.read_csv(db_path, sep=',', header=None)
    data = data.loc[data[4].isna()]
    id_list = data[1].values
    result = np.empty(len(id_list), dtype=object)
    vk_constraint = 25
    start = 0
    end = start + vk_constraint
    while start < len(id_list):
        request = get_friend_script(list(id_list[start:end]))
        result[start:end] = api.execute(code=request, v='5.126')
        start = end
        end = start + vk_constraint
        time.sleep(2)
        if end >= len(id_list):
            end = len(id_list)
    output = pd.DataFrame(columns=['id', 'friends'])
    output['id'] = id_list
    output['friends'] = result
    output.to_csv(f'{output_name}.csv')
    print(time.time() - start_time)


session = vk.AuthSession(app_id=ID, user_login=LOGIN, user_password=PASSWORD)
api = vk.API(session)
get_friends("Nsk_2003.csv", 'nsk_2003_friends')
