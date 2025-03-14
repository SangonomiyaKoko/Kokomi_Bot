def aid2rid(account_id: int):    
    account_id_len = len(str(account_id))
    # 俄服 1-9 [~5字段]
    if account_id_len < 9:
        return 4
    elif (
        account_id_len == 9 and 
        int(account_id/100000000) in [1,2,3]
    ):
        return 4
    # 欧服 9 [5~字段] 
    if (
        account_id_len == 9 and
        int(account_id/100000000) in [5,6,7]
    ):
        return 2
    # 亚服 10 [2-3字段]
    if (
        account_id_len == 10 and
        int(account_id/1000000000) in [2,3]
    ):
        return 1
    # 美服 10 [1字段]
    if (
        account_id_len == 10 and
        int(account_id/1000000000) in [1]
    ):
        return 1
    # 国服 10 [7字段]
    if (
        account_id_len == 10 and
        int(account_id/1000000000) in [7]
    ):
        return 5
    return None

ids = [500046717,676858927,701045652]
res = []
for id in ids:
    res.append(aid2rid(id))
print(res)