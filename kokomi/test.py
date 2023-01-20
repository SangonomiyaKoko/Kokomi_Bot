import sys
import os
import asyncio
import json
import httpx
import requests
from .scripts.ship import ship
from .scripts.recent import recent
from .scripts.contribution import contribution
from .scripts.name import name
from .scripts.set import set

account_id = 2023619512
ship_id = 4181604048
server = 'asia'
date = 7
recent_type = 'pvp'

# account_id = 2036916997
# ship_id = 3751196368
# server = 'asia'
# date = 1
# recent_type = 'pvp'


seach_str = 'ss'
add_standardname = 'u-2501'
add_nickname = '2501'
'''模块测试'''

# 1.wws me ship
print(asyncio.run(ship.pic([server, account_id, ship_id]).main()))

# 2.wws me recent
print(recent.pic().main(recent_type, asyncio.run(
    recent.recent((account_id, server, date)).recent_data())))

# 3.wws 日历
print(asyncio.run(contribution.pic((account_id, server)).main()))

# 5.wws seach/wws add
print(name.seach_name().main(seach_str))
#print(name.add_name().main(add_standardname, add_nickname))

# 6.set
print(asyncio.run(set.bind().set_id('3197206779', 'sangonomiyakokomi_', 'asia')))
