from ..utils.assets_converter import convert_price
async def build_custom_info(account_snapshot):
    custom_info = {
        "last_update":account_snapshot["snapshotVos"][0]["updateTime"],
        "list":[
            {
                "asset":crypto["asset"],
                 "free": crypto["free"],
                "locked":crypto["locked"],

            } for crypto in account_snapshot["snapshotVos"][0]["data"]["balances"]
        ]
    }
    return custom_info

async def get_wallet_info(client, account_snapshot):
    custom_info = await build_custom_info(account_snapshot)
    # print("getting custom info in get_wallet_info", custom _info)
    for crypto in custom_info["list"]:
        price, currency = await convert_price(client, crypto["asset"], crypto["free"])
        crypto["converted_price"] = price
        crypto["currency"] = currency
    return custom_info