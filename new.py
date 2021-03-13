import csv
import vk
import time
import numpy as np
import pandas as pd
from config import LOGIN, PASSWORD, ID, ACCESS_TOKEN
from vk_script import modify_script, get_friend_script


def write_data(city_name: str, source: str, year: int) -> None:
    """
    Function for writing response from vk method users.search
    :param city_name: city name
    :param source: string, path to created file
    :param year: int, birth year of vk users
    :return: None
    """
    parse = source.split(',')
    current_pos = 0
    end = 6
    with open(f'{city_name}_{year}.csv', 'w', newline='', encoding='utf-8') as output:
        id_writer = csv.writer(output, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        while end < len(parse):
            id_writer.writerow(parse[current_pos:end])
            current_pos = end
            end = current_pos + 6
            if end >= len(parse):
                end = len(parse)


def mine_users(start_year: int, end_year: int, city_code: int, city_name: str) -> None:
    """
    Function for mining vk users from vk api
    :param city_name: city name
    :param start_year: start birth year of vk users range
    :param end_year: end birth year of vk users range
    :param city_code: city code from vk api
    :return: None
    """
    start = time.time()
    while start_year >= end_year:
        request = modify_script(city_code, start_year)
        data = api.execute(code=request, v="5.126")
        time.sleep(1)
        write_data(city_name, data, start_year)
        start_year -= 1
    print(time.time() - start)


def get_user_id(file_path: str, column: int, foreign_import=False) -> list:
    """
    Function for getting user's id from csv file that was created from
    mine_users() instance
    :param file_path: path to the csv file
    :param column: column for dropping na users
    :return: id list
    """
    data = pd.read_csv(file_path, sep=',', header=None)

    if foreign_import:
        data.dropna(how='all', inplace=True)
        return data[0].values

    else:
        data = data.loc[data[column].isna()]
        data.dropna(how='all', inplace=True)
        return data[1].values


def write_friends_count_to_csv(output_name: str, id_list: list, friends_count: np.array, cities: list) -> None:
    """
    Support function for writing friends count to csv
    :param output_name: output filename
    :param id_list: list of vk user's id
    :param friends_count: amount of friends for every user
    :return: None
    """
    output = pd.DataFrame(columns=['id', 'friends', 'cities'])
    output['id'] = id_list
    output['friends'] = friends_count
    output['cities'] = cities
    output.to_csv(f'{output_name}.csv')


def get_friends(db_path: str, output_name: str, foreign: bool) -> None:
    """
    Function for mining friends count for vk users
    :param db_path: path to the users data csv file
    :param output_name: output name for our file
    :return: None
    """
    start_time = time.time()

    id_list = []

    if foreign:
        id_list = get_user_id(db_path, column=4, foreign_import=True)

    else:
        id_list = get_user_id(db_path, column=4, foreign_import=False)

    result = np.empty(len(id_list), dtype=object)
    vk_constraint = 25
    start = 0
    end = start + vk_constraint
    while start < len(id_list):
        request = get_friend_script(list(id_list[start:end]))
        result[start:end] = api.execute(code=request, v='5.126')
        start = end
        end = start + vk_constraint
        time.sleep(1)
        if end >= len(id_list):
            end = len(id_list)

    friends = []
    cities = []

    for item in result:
        friends.append(item[0])
        users = item[1]
        friends_cities = []

        if users is None:
            cities.append(friends_cities)
            continue

        for i in range(len(users)):
            if 'city' in users[i]:
                friends_cities.append(users[i]['city']['title'])
        cities.append(friends_cities)

    write_friends_count_to_csv(output_name, id_list, friends, cities)
    print(time.time() - start_time)


session = vk.AuthSession(app_id=ID, user_login=LOGIN, user_password=PASSWORD)
api = vk.API(session)

#mine_users(start_year=1991, end_year=1986, city_code=721, city_name='Власиха')
get_friends('Балашиха.csv', 'Балашиха_friends', foreign=True)

"""
query = get_friend_script([1721420, 1668252])
done = api.execute(code=query, v='5.126')


write_friends_count_to_csv('output_name', [1721420, 1668252], friends, cities)
"""