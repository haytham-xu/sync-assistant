
def get_all_keys(dict_list):
    res = set()
    for d in dict_list:
        res.add(d.keys())
    return res
