import asyncio
import configparser
import numpy as np
from modules import getPrice as Price
from modules import getNpPriceStat as np_price
from modules.utils import assets_converter 
from modules.utils.customPrint import printC
from binance.spot import Spot
import datetime
#import matplotlib.pyplot as plt
from modules.wallet_ import sort_
import json

#!!! If base_url is not provided, it defaults to api.binance.com

crypto_pairs = (
    "ETHBTC",
    "BNBBTC",
    "LTCBTC",
    "BTCTUSD"
    # Add more crypto pairs as needed
)
async def get_credentials():
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    return config["keys"]["api_key"], config["keys"]["api_secret"]
  
crypto_conversion = (
        "EUR",
        "USDT",
        "BTC",
        "ETH"
    )    
    
def testi(client, crypto_conversion=crypto_conversion, index = 0):
    try:
        print(crypto_conversion[index])
        if index == len(crypto_conversion):
            print("finito")
        else:
            return client.ticker_24hr("LINK"+crypto_conversion[index])
    except Exception:
        return testi(client, crypto_conversion, index +1)


async def main():
    key, token = await get_credentials()
    client = Spot(api_key=key, api_secret=token)
    # client.ticker_24hr("RUBETH")
    # client.ticker_24hr("RUBEUR")
    # client.ticker_24hr("RUBUSDT")
    # SYMBOL = "RUBEUR"
    # try:
    #     client.ticker_24hr(SYMBOL)
    # except Exception:
    #     print(SYMBOL)

    account_snapshot = client.account_snapshot(type="SPOT")
    all_balances = []
    for i in account_snapshot["snapshotVos"][0]["data"]["balances"]:
        all_balances.append(i["asset"])
    # printC(account_snapshot)
    printC(len(all_balances),"BALANCES")
    wallet_info = await sort_.get_wallet_info(client, account_snapshot)
    # for i in account_snapshot["snapshotVos"][0]["data"]["balances"]:
    #     await assets_converter.convert_price(1,i["asset"],client)
    printC(wallet_info)
    import uuid

    def add_currencies_to_db(currency_list):
        try:
            conn = psycopg2.connect(f"dbname=suppliers user=postgres password=")
            cur = conn.cursor()
            custom_id = 0
            for el in currency_list["list"]:
                    if el["currency"] != "None" and el["converted_price"] != 999:
                        sql =  f"""INSERT INTO currency(currency_id,currency_name,current_value,currency_in)
                                 VALUES ({custom_id}, '{el["asset"]}', {el["converted_price"]}, '{el["currency"]}') RETURNING currency_id;"""
                        cur.execute(sql)
                        custom_id = custom_id + 1
                        conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except Exception as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()                    
    add_currencies_to_db(wallet_info)


            
    # custom_info = await get_currency(account_snapshot)
    excludenone = []
    for i in wallet_info["list"]:
        if i["converted_price"] == 999:
            excludenone.append(i)
    # printC("*****************\n",excludenone,"\n*****************EXCLUDE NONE")
    # print('Nested List :', json.dumps(coin_info, indent=4))
    # parsed = json.dumps('''{}'''.format(coin_info),indent=4)
    # printC(coin_info)
    # printC(account_snapshot)
    start_date_time = datetime.datetime.now()
    end_date_time = datetime.datetime(2023, 7, 13, 2, 0, 0, 0)
    average_price_eth_btc = Price.get_average_price_in_time_range("ETHBTC",client,start_date_time,end_date_time,5)
    # average_price_bnb_btc = Price.get_average_price_in_time_range("BNBBTC",client,start_date_time,end_date_time,600)
    average_price_eth_btc = await asyncio.gather(average_price_eth_btc)#,average_price_bnb_btc)
    # print(average_price_eth_btc[0])
    # average_price_eth_btc = np.array(average_price_eth_btc)
    # average_price_bnb_btc = np.array(average_price_bnb_btc)
    # function to store the data given an array 
   
    # plt.hist(average_price_eth_btc)
    # plt.show()
    # storage_prices = np.array([])
    # storage_average_prices = np.array([await Price.get_all_average_prices(crypto_pairs,client)])
    # print(storage_average_prices,"AVERAGE PRICES")
    # singles = await np_price.create_single_np_price_stat("BTCTUSD", await Price.get_all_prices(crypto_pairs, client))
    # reportBtcUsdt = np_price.create_np_price_report(client, crypto_pairs, "ETHBTC", storage_prices, start_date_time, end_date_time, 240)
    # reportBnbBtc = np_price.create_np_price_report(client, crypto_pairs, "BNBBTC", storage_prices, start_date_time, end_date_time, 240)
    # reportBtcUsdt,reportBnbBtc = await asyncio.gather(reportBtcUsdt,reportBnbBtc)



asyncio.run(main())