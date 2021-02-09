
def modify_script(city_code: int, year: int):
    """
    Support function for modifying vk script
    :param city_code: vk city code
    :param year: birth year of vk users
    :return: complete vkscript
    """

    head = 'var members = API.users.search({"q":"", "city":%d, "birth_year":%d, \
            "birth_month":1, "sex": 1, "count":"1000", "v": "5.126"}).items;' % (city_code, year)

    body = ' var month = 2; \
       var gender = 1; \
       while (month <= 12 && gender <= 2) \
       { \
         if (month == 12) { \
           gender = gender + 1; \
           month = 1; \
         } \
         members = members + "," + API.users.search({"q":"", "city":%d, "birth_year":%d, \
               "birth_month":month, "count":"1000", "v": "5.126"}).items; \
         month = month + 1; \
       };\
       return members;' % (city_code, year)

    return head + body


def get_friend_script(id_list: list):
    """
    Support function for modifying vkscript
    :param id_list: vk_id list
    :return: complete vkscript
    """
    array = f'var a = {id_list};'

    body = 'var index = 0;\
           var result = [];\
           while (index < %d){\
           result.push(API.friends.get({"user_id":a[index],\
           "order":"name",  "count":0, "offset":1, "v":"5.126"}).count);\
           index = index + 1;' \
          '};\
          return result;' % (len(id_list))

    return array + body

