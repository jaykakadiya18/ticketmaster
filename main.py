# import concurrent.futures
# import requests
# import time
# import json
# import pandas as pd

# # Tor proxy settings
# tor_proxy = {
#     'http': 'http://geo.iproyal.com:12321'
# }
# output_li = []

# with open("result.json", "w") as json_file_dump:
#     json.dump([{"data":"data"}], json_file_dump)


# def make_tor_request(url, event):
#     try:
#         querystring = {
#             "show":"listpricerange",
#             "by":"offers inventoryTypes accessibility section",
#             "apikey":"b462oi7fic6pehcdkzony5bxhe",
#             "apisecret":"pquzpfrfz7zd2ylvtz3w5dtyse"
#             }
#         payload = ""
#         headers = {
#             'User-Agent': "user-agent=Mozilla/5.0 (Linux; Android 11; 10011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36",
#             'Accept': "*/*",
#             'Accept-Language': "en-US,en;q=0.5",
#             'Accept-Encoding': "gzip, deflate, br",
#             'TMPS-Correlation-Id': "4c6c3d21-840b-455f-a499-eacf967ae948",
#             'Origin': "https://www.ticketmaster.com",
#             'Connection': "keep-alive",
#             'Referer': "https://www.ticketmaster.com/",
#             'Sec-Fetch-Dest': "empty",
#             'Sec-Fetch-Mode': "cors",
#             'Sec-Fetch-Site': "same-site",
#             'If-Modified-Since': "Tue, 14 Jun 2022 04:09:45 GMT",
#             'If-None-Match': 'W/"006e0bc54a443a39eaf1c15ede4e46e08"',
#             'TE': "trailers"
#             }
#         flag = True
#         while flag:
#             # with requests.Session() as session:
#                 # session.proxies = tor_proxy

#             # url = "http://api.scraperapi.com?api_key=1be2df3532158d96153ff0f0c0760153&url=" + url
#             # response = session.request("GET", url, data=payload, headers=headers, params=querystring)
#             # print(url)
#             response = requests.request("GET", url, proxies= tor_proxy, headers=headers, data=payload, params=querystring)
#             print(response.text)
#             # response = session.request("GET", url)
#             # print(response.text)
#             response_text =  json.loads(response.text)
#             meta_value = response_text.get("title", "nothing")
#             if meta_value!="403 Internal Error" and meta_value!="It's not you - it's us":
#                 output_li.append(response_text)
#                 print(response_text)
#                 flag=False

#     except Exception as e:
#         print(e)

# df = pd.read_csv("event_id.csv", header=None, skiprows=1, names=["event_id"])

# worker_length = int(df.shape[0]/1)
# # worker_length = 1
# executor = concurrent.futures.ThreadPoolExecutor(max_workers=worker_length)

# threads = []
# start = 0
# end = worker_length
# count_add = worker_length

# start_time = time.time()
# main_flag = True
# data = list(df["event_id"])
# while main_flag:
#     if end>=df.shape[0]:
#         end = df.shape[0]
#         main_flag=False
#     for ev in data[start:end]:
#         url = f"https://offeradapter.ticketmaster.com/api/ismds/event/{ev}/facets"
#         threads.append(executor.submit(make_tor_request, url, ev))

#     concurrent.futures.wait(threads)
#     start = end
#     end+=count_add

# with open("result.json", "r") as json_file:
#     all_json_data = json.load(json_file)
#     json_data = list(all_json_data)
#     json_data.extend(output_li)

# with open("result.json", "w") as json_file_dump:
#     json.dump(json_data, json_file_dump)
# print(f"total time {time.time()-start_time}")
# print("completed")

import asyncio
import aiohttp
import time
import json
import pandas as pd

tor_proxy = 'http://geo.iproyal.com:12321'
output_li = []

start_time = time.time()

async def make_tor_request(session, url, ev):
    try:
        querystring = {
            "show": "listpricerange",
            "by": "offers inventoryTypes accessibility section",
            "apikey": "b462oi7fic6pehcdkzony5bxhe",
            "apisecret": "pquzpfrfz7zd2ylvtz3w5dtyse"
        }
        payload = ""
        headers = {
            'User-Agent': "user-agent=Mozilla/5.0 (Linux; Android 11; 10011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36",
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'TMPS-Correlation-Id': "4c6c3d21-840b-455f-a499-eacf967ae948",
            'Origin': "https://www.ticketmaster.com",
            'Connection': "keep-alive",
            'Referer': "https://www.ticketmaster.com/",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'If-Modified-Since': "Tue, 14 Jun 2022 04:09:45 GMT",
            'If-None-Match': 'W/"006e0bc54a443a39eaf1c15ede4e46e08"',
            'TE': "trailers"
        }

        flag = True
        while flag:
            async with session.get(url, params=querystring, headers=headers) as response:
                response_text = await response.json()
                meta_value = response_text.get("title", "nothing")
                if meta_value != "403 Internal Error" and meta_value != "It's not you - it's us":
                    print(response_text)
                    output_li.append(response_text)
                    flag = False

    except Exception as e:
        print(e)

async def main():
    df = pd.read_csv("event_id.csv", header=None, skiprows=1, names=["event_id"])
    worker_length = int(df.shape[0] / 1)

    connector = aiohttp.TCPConnector(ssl=False, limit_per_host=worker_length)
    
    async with aiohttp.ClientSession(connector=connector, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 11; ...)'}) as session:
        tasks = []

        for ev in df["event_id"]:
            print(ev)
            url = f"https://offeradapter.ticketmaster.com/api/ismds/event/{ev}/facets"
            tasks.append(make_tor_request(session, url, ev))

        await asyncio.gather(*tasks)

asyncio.run(main())

with open("result.json", "r") as json_file:
    all_json_data = json.load(json_file)
    json_data = list(all_json_data)
    json_data.extend(output_li)

with open("result.json", "w") as json_file_dump:
    json.dump(json_data, json_file_dump)

print(f"total time {time.time()-start_time}")
print("completed")
