import json

import config
import time


def save_json(response_list):
    for coin_id, currency_data in response_list.items():
        responses = []
        for api_call in currency_data:
            if len(api_call['Data']) == 0:
                pass

            d = api_call['Data']

            response = {"time": d["time"], "value": d["high"]}
            responses.append(response)

        with open(f"{find_coin(coin_id)}_{time.time()}.json", 'w') as f:
            f.write(json.dumps(responses))


def find_coin(coin_id):
    currencies = config.Configuration.config["currencies"]

    for coin in currencies:
        if coin["id"] == coin_id:
            return coin["coin"]