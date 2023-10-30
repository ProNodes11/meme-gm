import aiohttp
from better_automation import TwitterAPI
import aiohttp_socks
import asyncio
import random
import time

async def twitter_demo_with_proxy(auth_token, proxy_url):
    connector = aiohttp_socks.ProxyConnector.from_url(proxy_url)
    async with aiohttp.ClientSession(connector=connector) as session:
        twitter = TwitterAPI(session, auth_token)
        username = await twitter.request_username()
        print(f"Your username: {username}")

        twitt_ID = 1718788079413244315
        try:
            print(f"Tweet {twitt_ID} is replied. Reply id: {await twitter.reply(twitt_ID, 'GM')}")
        except Exception as e:
            print(f"Error: {e}")
            with open("result.csv", "a") as file:
                line = f"{auth_token},{proxy_url},Failed\n"
                file.write(line)
            return

        with open("result.csv", "a") as file:
            line = f"{auth_token},{proxy_url},Succsess\n"
            file.write(line)

class MyStruct:
    def __init__(self, proxy, token):
        self.proxy = proxy
        self.token = token

data_array = []

with open("proxy.txt", "r") as proxy_file, open("token.txt", "r") as token_file:
    for proxy_line, token_line in zip(proxy_file, token_file):
        proxy = proxy_line.strip() 
        token = token_line.strip()  

        my_struct = MyStruct(proxy, token)
        data_array.append(my_struct)

async def main():
    for item in data_array:
        random_delay = random.uniform(1, 3)
        try:
            await twitter_demo_with_proxy(item.token, item.proxy)
        except Exception as e:
            continue    
        time.sleep(random_delay)
        

asyncio.run(main())