import aiohttp
from dotenv import dotenv_values
import json


async def get_data(api_versions:list[int], token:str=None, max_page_size=1200) -> list[dict]:
    """
    If there is more than 1235 accomodations available on the api, if we ask more than 1235 the api sends no content back because too much was requested
    Provide token if you need to test it
    """

    if token is None: token = dotenv_values(".env")["CROUS_TOKEN"]

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
        "Referer": f"https://trouverunlogement.lescrous.fr/tools/residual/27/search",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    data = []
    async with aiohttp.ClientSession(headers=headers) as session:
        for api_version in api_versions:
            data += await request(session, api_version, max_page_size)
    
    return data


async def request(session: aiohttp.ClientSession, api_version: int, max_page_size: int, page=1) -> list[dict]:
    """
    api_version: 27 means year 2022-2023 and 29 2023-2024
    page: sometimes there are more free accomodations than what it is possible to display on one page, so many pages are needed. While our current page is not empty, we request the next page.
    """

    url = f'https://trouverunlogement.lescrous.fr/api/fr/search/{api_version}'
    body= "{\"precision\":6,\"need_aggregation\":true,\"page\":"f"{page}"",\"pageSize\":"f"{max_page_size}"",\"sector\":null,\"idTool\":"f"{api_version}"",\"occupationModes\":[],\"equipment\":[],\"price\":{\"min\":0,\"max\":null},\"location\":[{\"lon\":-5.4534,\"lat\":51.2683},{\"lon\":9.8678,\"lat\":41.2632}]}"

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

    # there are many ['set-cookie'] in the headers got with aiohttp

    if "SimpleSAMLSessionID" in str(headers):
        raise TokenDead


class TokenDead(Exception):
    pass