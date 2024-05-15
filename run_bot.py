import asyncio
from Kokomi_Bot.command_select import select_funtion

async def main():
    result = await select_funtion.main(
        msg = ['wws','help'],
        user_id = '319720677',
        user_data = {},
        platform = 'qq_bot',
        platform_id = '123456',
        channel_id = '123456',
        platform_data = {}
    )
    return_type = result['type']
    return_data = result[return_type]
    print(return_type.upper(),return_data)

asyncio.run(
    main()
)
