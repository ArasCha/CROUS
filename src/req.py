import aiohttp
from dotenv import dotenv_values
import json

ile_de_france_bounds = "[{\"lon\":1.8759155273437502,\"lat\":49.017157315497165},{\"lon\":2.9278564453125,\"lat\":48.671012624325996}]"

async def get_data(api_versions:list[int], token:str=None, max_page_size=200) -> list[dict]:
    """
    If there is more than max_page_size accomodations available on the api, if we ask more than max_page_size the api sends no content back because too much was requested
    Provide token if you need to test it
    """

    if token is None: token = dotenv_values(".env")["CROUS_TOKEN"]

    headers = {
        "accept": "application/ld+json, application/json",
        "accept-language": "fr",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"_pk_id.1.5ea2=0dec6f58d11b9f93.1698746180.; HAPROXYID=app3; PHPSESSID={token}; qpid=cqac4r3fm5tsvkruskbg",
        "Referrer": "https://trouverunlogement.lescrous.fr/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    data = []
    async with aiohttp.ClientSession(headers=headers) as session:
        for api_version in api_versions:
            data += await request(session, api_version, max_page_size)
    
    return data


async def request(session: aiohttp.ClientSession, api_version: int, max_page_size: int, page=1) -> list[dict]:

    url = f'https://trouverunlogement.lescrous.fr/api/fr/search/{api_version}'
    body = "{\"idTool\":"f"{api_version}"",\"need_aggregation\":true,\"page\":"f"{page}"",\"pageSize\":"f"{max_page_size}"",\"sector\":null,\"occupationModes\":[],\"location\":"f"{ile_de_france_bounds}"",\"residence\":null,\"precision\":6,\"equipment\":[],\"adaptedPmr\":false,\"toolMechanism\":\"residual\"}"

    async with session.post(url, data=body) as response:
        
        check_token(response.headers)
        try:
            data = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            print(f"Nothing in the response (litterally nothing) by requesting the api {api_version}, the provided size of {max_page_size} is too big")
            return []

    if data['results']['items'] == []:
        return []

    return data['results']['items'] + await request(session, api_version, max_page_size, page=page+1)


def get_data_simulation() -> list[dict]:

    with open("../available.json", "r", encoding="utf-8") as f:
        content = f.read()
    
    return json.loads(content)


def check_token(headers: aiohttp.ClientResponse.headers):

    if "PHPSESSID=deleted" in str(headers):
        raise TokenDead


class TokenDead(Exception):
    pass
