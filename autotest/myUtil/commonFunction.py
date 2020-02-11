import datetime
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
