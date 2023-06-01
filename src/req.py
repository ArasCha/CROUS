import aiohttp
from dotenv import dotenv_values
import json


async def get_data() -> list[dict]:

    token = dotenv_values(".env")["CROUS_TOKEN"]

    data = await request(token, 27) + await request(token, 29) # year 2022-2023 and 2023-2024
    print(len(data))

    return data


async def request(token: str, api_version: int) -> list[dict]:

    url = f'https://trouverunlogement.lescrous.fr/api/fr/search/{api_version}'

    headers = {
        "accept": "application/ld+json, application/json",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"SimpleSAMLSessionID=7cf93d422831c329e57766caeb86ec57; HAPROXYID=app4; PHPSESSID={token}; qpid=cb78nvjfm5tsme57c3cg",
        "Referer": f"https://trouverunlogement.lescrous.fr/tools/residual/{api_version}/search",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    max_size = 1235
    # If there is more than 1235 accomodations available on the api, if we ask more than 1235 the api sends no content back

    body= "{\"precision\":6,\"need_aggregation\":true,\"page\":1,\"pageSize\":"f"{max_size}"",\"sector\":null,\"idTool\":"f"{api_version}"",\"occupationModes\":[],\"equipment\":[],\"price\":{\"min\":0,\"max\":null},\"location\":[{\"lon\":-5.4534,\"lat\":51.2683},{\"lon\":9.8678,\"lat\":41.2632}]}"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=body) as response:
            check_token(response.headers)
            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Nothing in the response (litterally nothing) by requesting the api {api_version}, the provided size of {max_size} is too big")
                return []
    

    return data['results']['items']


def get_data_simulation() -> list[dict]:

    with open("../available.json", "r", encoding="utf-8") as f:
        content = f.read()
    
    return json.loads(content)


def check_token(headers: aiohttp.ClientResponse.headers):

    # there are many ['set-cookie'] in the headers get with aiohttp

    if "SimpleSAMLSessionID" in str(headers):
        raise TokenDead
    

class TokenDead(Exception):
    pass