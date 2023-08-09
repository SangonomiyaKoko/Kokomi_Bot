import asyncio
import traceback
#from kokomi_bot.command_select import select_funtion
from nonebot_plugin_kokomi.command_select import select_funtion
user_id = '3197206779'
message = 'wws me'
user_list = {
    '3197206779': 'test_account_0',
    '1835185912': 'test_account_1',
    '1295288371': 'test_account_2',
    '1817434987': 'test_account_3',
    '893413397': 'test_account_4',
    '860282373': 'test_account_5',
    '2979465540': 'test_account_6',
    '3075078697': 'test_account_7',
    '1937747784': 'test_account_8',
    '13648805': 'test_account_9',
    '531529798': 'test_account_10'
}


async def main():
    try:
        qq_id = user_id
        split_msg = message.split()
        if len(split_msg) == 1:
            return False
        gruop_id = '677135822'
        group_name = 'None'
        group_data = None
        if gruop_id != None and 'group' in split_msg:
            group_data = user_list
            group_info = [{'group_id': 164933984,
                           'group_name': 'Kokomi的寄寄子交流群'}]
            for index in group_info:
                if str(index['group_id']) == gruop_id:
                    group_name = index['group_name']
                else:
                    continue
        fun = await select_funtion.main(
            message=split_msg,
            user_id=qq_id,
            group_id=gruop_id,
            group_name=group_name,
            group_data=group_data
        )
        if fun['status'] == 'default':
            print('DEFAULT:', '无对应功能')
        elif fun['status'] == 'info':
            print('INFO:', fun['message'])
        else:
            function = fun['function']
            result = await function(fun['parameter'])
            if result['status'] == 'ok':
                print('OK', '发送图片')
            elif result['status'] == 'info':
                print('INFO:', result['message'])
            else:
                print('ERROR:', result['message'])
        return False
    except Exception:
        print(traceback.format_exc())


def group_data_formate(group_data: dict):
    processed_data = {}
    for group_member in group_data:
        processed_data[group_member['user_id']] = group_member['nickname']
    return processed_data


if message.startswith('wws'):
    asyncio.run(main())
