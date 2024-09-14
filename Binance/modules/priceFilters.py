import asyncio
def get_price(symbol, client, max_retry = 3, retry = 0):
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
            return get_price(symbol,client, max_retry, retry + 1)