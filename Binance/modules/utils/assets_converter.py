from ..getPrice import get_ticker
async def convert_price(client, single_or_crypto_pair, amount = 1):
    price_data, currency = await get_ticker(client, single_or_crypto_pair)
    print(amount,price_data["price"])
    return float(amount) * float(price_data["price"]), currency