import datetime,json
#遍历字典中的所有value，如果遇到datetime类型的，转化为字符串
def turn_dic_to_be_JSON_serializable(dic):
    # print("dic:", dic)
    for key in dic:
        # print(key , type(dic[key]))
        if type(dic[key]) == datetime.datetime:
            # datestr =  dic[key].strftime("%Y-%m-%d %H:%M:%S")
            # print('datestr:',datestr)
            dic[key] = dic[key].strftime("%Y-%m-%d %H:%M:%S")

    return dic

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
