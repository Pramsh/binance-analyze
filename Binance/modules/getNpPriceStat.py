import asyncio
import numpy as np
import datetime
import os
import sys
from modules.getPrice import get_all_prices
async def create_single_np_price_stat(symbol, list_of_info, max_retry = 3, retry = 0):
    try:
        ts = list_of_info[0]["closeTime"] / 1000
        print(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),"\nDATE TIME")
        arr = np.array([[info["highPrice"], info["lowPrice"]] for info in list_of_info if info["symbol"] == symbol])
        if len(arr) == 0:
            raise Exception("An error occured -- PROBABLY THE SYMBOL IS NOT PRESENT IN THE CRYPTO_PAIRS TUPLA")

        return arr
    except Exception:
        if retry <= max_retry:
            print("handling err")
            await asyncio.sleep(2) 
            return await create_single_np_price_stat(symbol, list_of_info, max_retry, retry + 1)
        else:
            raise Exception("An error occured in create_single_np_price_stat")
        
async def create_np_price_report(client, crypto_pairs, symbol, storage_prices, start_date_time, end_date_time, time_interval = 120, retry_interval = 300, max_retry = 3, retry = 0):
    list_of_info = []
    try:
        # print(dir(modules.getPrice))
        while start_date_time < end_date_time:
            
            list_of_info = await get_all_prices(crypto_pairs, client) #get recent data from binance
            recent_prices = await create_single_np_price_stat(symbol, list_of_info)
            if storage_prices.size == 0:
                storage_prices = recent_prices  # Assign recent_prices directly
            else:        
                storage_prices = np.concatenate((storage_prices, recent_prices))
                print("storage_prices\n",storage_prices)
            start_date_time = datetime.datetime.now()
            await asyncio.sleep(time_interval)    
        return storage_prices, 
    except Exception:
        if retry <= max_retry:
            print("handling err")
            await asyncio.sleep(2) 
            return await create_np_price_report(client, crypto_pairs, symbol, storage_prices, start_date_time, end_date_time, max_retry, retry + 1)
        else:
            raise Exception("An error occured in create_np_price_report")
            

            
def foo(file):
    # print(dir(Price),"DIOLORDO")
     # csfp - current_script_folder_path
    csfp = os.path.abspath(os.path.dirname(file))
    print(dir(csfp))
    if csfp not in sys.path:
        sys.path.insert(0, csfp)
    else:
        print("c'è")    
# import it and invoke it by one of the ways described above