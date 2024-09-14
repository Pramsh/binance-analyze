import asyncio
import datetime 


default_crypto_conversion = (
    "EUR",
    "USDT",
    "BTC",
    "ETH"
)


async def get_price(symbol, client, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve the current price,
    according to a crypto pair.
    *********
    The required parameters are:
        - symbol:string = cryto pair
        . client:Spot = binance Spot 
    """
    try:
        return client.ticker_24hr(symbol)
    except Exception:
        if retry <= max_retry:
            await asyncio.sleep(2) 
            return await get_price(symbol,client, max_retry, retry + 1)
        else:
            raise Exception("ERROR")
            
            
def check_crypto_exception(crypto_pair, default_symbol):
    return crypto_pair, "None"        


            
def check_for_default_symbol(symbol, default_symbol):
    if  len(symbol) == 6: 
        return symbol, symbol[:3] 
    elif len(symbol) == 3 or len(symbol) == 4:
        return symbol + default_symbol, default_symbol
    elif len(symbol) >= 7 or len(symbol) == 5: ## tutte quelle con 7 si fermano cosi, che è giusto per il mapping
        return symbol, "None"   
    else:
        return symbol, "None"





async def get_ticker(client, symbol, default_symbol = "EUR", alternative_default_symbols = default_crypto_conversion, index = 0, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve the current price,
    according to a crypto pair.
    *********
    The required parameters are:
        - symbol:string = cryto pair
        . client:Spot = binance Spot 
    """
    try:
        
        for asset in default_crypto_conversion:
            if asset != symbol:
                pair_symbol, currency = check_for_default_symbol(symbol, default_symbol)
                res = client.ticker_price(pair_symbol), currency
                return res
            else:
                return {"price":999}, "None"    
    except Exception:
        if len(symbol) >= 3 or len(symbol) <= 5:
            if default_symbol !=  default_crypto_conversion[-1]:
                return await get_ticker(client, symbol, default_crypto_conversion[index], alternative_default_symbols, index +1)
            else:
                return {"price":999}, "None"               
        else:
            if retry <= max_retry:
                await asyncio.sleep(2)
                return await get_ticker(client, symbol, default_symbol,  max_retry, alternative_default_symbols, max_retry, retry + 1)
            else:
                raise Exception("PORCODIOERROR")
    
    
    
async def get_all_prices(crypto_pairs, client, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve all current prices
    according the list of crypto_pairs passed as first argument.
    *********
    The required parameters are:
        . crypto_pairs:list = crypto pairs to retrive the prices of
        . client:Spot = binance Spot 
    """
    try:
        return await asyncio.gather(*[get_price(pair,client) for pair in crypto_pairs])
    except Exception:
        if retry <= max_retry:
            await asyncio.sleep(2) 
            return await get_all_prices(crypto_pairs, client, max_retry, retry + 1)
        else:
            raise Exception("ERROR")


            
async def get_average_price(symbol, client, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve all current prices
    according the list of crypto_pairs passed as first argument.
    *********
    The required parameters are:
        . crypto_pairs:list = crypto pairs to retrive the prices of
        . client:Spot = binance Spot 
    """
    try:
        price_data = client.avg_price(symbol)
        return {
            "symbol":symbol,
            "average_price":price_data["price"],
            "timestamp":datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
    except Exception:
        if retry <= max_retry:
            await asyncio.sleep(2) 
            return await get_average_price(symbol, client, max_retry, retry + 1)
        else:
            raise Exception("ERROR")


            
            
async def get_average_price_in_time_range(symbol, client, start_date, end_date, time_interval = 300, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve all current prices
    according the list of crypto_pairs passed as first argument.
    *********
    The required parameters are:
        . crypto_pairs:list = crypto pairs to retrive the prices of
        . client:Spot = binance Spot 
    """
    try:
        prices_list = []
        while start_date < end_date:
            start_date = datetime.datetime.now()
            prices_list.append(await get_average_price(symbol, client))
            print("ok -- at ", start_date, "\nRES:\n", prices_list[-1])
            await asyncio.sleep(time_interval)
        return prices_list    
        return res
    except Exception:
        if retry <= max_retry:
            await asyncio.sleep(2) 
            return await get_average_price_in_time_range(symbol, client, start_date, end_date, time_interval, max_retry, retry + 1)
        else:
            raise Exception("ERROR")            
    
    
    
async def get_all_average_prices(crypto_pairs, client, max_retry = 3, retry = 0):
    """
    This function is usefull to retrieve all the average prices
    according the list of crypto_pairs passed as first argument.
    *********
    The required parameters are:
        . crypto_pairs:list = crypto pairs to retrive the prices of
        . client:Spot = binance Spot 
    """
    try:
        return await asyncio.gather(*[get_average_price(pair,client) for pair in crypto_pairs])
    except Exception:
        if retry <= max_retry:
            await asyncio.sleep(2) 
            return await get_all_average_prices(crypto_pairs, client, max_retry, retry + 1)
        else:
            raise Exception("ERROR")
        