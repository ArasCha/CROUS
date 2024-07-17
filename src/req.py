import aiohttp
from dotenv import dotenv_values
import json

ile_de_france_bounds = "[{\"lon\":1.8759155273437502,\"lat\":49.017157315497165},{\"lon\":2.9278564453125,\"lat\":48.671012624325996}]"
orleans_bounds = "[{\"lon\":1.8355680963101053,\"lat\":47.92474001024498},{\"lon\":1.942341472774949,\"lat\":47.88066424009748}]"
occupation_mode = "[\"alone\"]"


class CrousSession:
    
    def __init__(self, api_version: int):
        self.api_version = api_version
        self.token = dotenv_values(".env")["CROUS_TOKEN"]
        self.session: aiohttp.ClientSession = None
    
    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.get_headers(self.token))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.session = None
         
    def get_headers(self, token:str):
        return {
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
    
    async def test_token(self, token:str) -> bool:
        
        headers = self.get_headers(token)
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=body) as response:
                try:
                    check_token(response.headers)
                except TokenDead:
                    return False
                return True


    async def get_free_accommodations(self, max_page_size = 500, page=1) -> list[dict]:
        """
        max_page_size: sometimes there are more free accommodations than what it is possible to display on one page, so many pages are needed. While our current page is not empty, we request the next page.
        """

        url = f'https://trouverunlogement.lescrous.fr/api/fr/search/{self.api_version}'
        body = "{\"idTool\":"f"{self.api_version}"",\"need_aggregation\":true,\"page\":"f"{page}"",\"pageSize\":"f"{max_page_size}"",\"sector\":null,\"occupationModes\":"f"{occupation_mode}"",\"location\":"f"{orleans_bounds}"",\"residence\":null,\"precision\":6,\"equipment\":[],\"adaptedPmr\":false,\"toolMechanism\":\"residual\"}"

        async with self.session.post(url, data=body) as response:
            
            check_token(response.headers)
            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Nothing in the response (litterally nothing) by requesting the api {self.api_version}, the provided size of {max_page_size} is too big")
                return []

        if data['results']['items'] == []:
            return []

        return data['results']['items'] + await self.get_free_accommodations(max_page_size, page=page+1)
    
    
    async def add_accommodation_to_selection(self, accommodation_id: int): # works
    
        url = f"https://trouverunlogement.lescrous.fr/api/fr/tools/{self.api_version}/carts/5112591/items"
        body = "{\"accommodation\":"f"{accommodation_id}""}"
        
        async with self.session.post(url, data=body) as response:
            if response.status == 200:
                print(accommodation_id, "added to selection")
                
            else: print("error while adding", accommodation_id, "to selection", response.text)


    async def book_accommodation(self, accommodation_id: int):

        url = f"https://trouverunlogement.lescrous.fr/api/fr/tools/{self.api_version}/requests"
        body  = (
            "------WebKitFormBoundaryIjfClOzXWcnYRqci\r\n"
            "Content-Disposition: form-data; name=\"request_submit[occupationMode]\"\r\n\r\n"
            "alone\r\n"
            "------WebKitFormBoundaryIjfClOzXWcnYRqci\r\n"
            f"Content-Disposition: form-data; name=\"accommodation\"\r\n\r\n"
            f"{accommodation_id}\r\n"
            "------WebKitFormBoundaryIjfClOzXWcnYRqci--\r\n"
        )
        
        self.session.headers["content-type"] = "multipart/form-data; boundary=----WebKitFormBoundaryIjfClOzXWcnYRqci"
        print(self.session.headers)
        
        async with self.session.post(url, data=body) as response:
            if response.status == 200:
                print(accommodation_id, "booked")
                
            else: print("error while booking", accommodation_id, await response.text())



def get_data_simulation() -> list[dict]:

    with open("../available.json", "r", encoding="utf-8") as f:
        content = f.read()
    
    return json.loads(content)


def check_token(headers: aiohttp.ClientResponse.headers):

    if "PHPSESSID=deleted" in str(headers):
        raise TokenDead


class TokenDead(Exception):
    pass


async def test():
    
    headers = {
        "accept": "*/*",
        "accept-language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,de-DE;q=0.5,de;q=0.4",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryIjfClOzXWcnYRqci",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "HAPROXYID=app4; qpid=cqbolujfm5tsvkt479o0; PHPSESSID=rv2p555cj5srbva67v4ugasgfj",
        "Referer": "https://trouverunlogement.lescrous.fr/tools/36/cart/requests/create/1314",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        
        url = "https://trouverunlogement.lescrous.fr/api/fr/tools/36/requests"

        accommodation_id = 1314
        data = (
            "------WebKitFormBoundaryIjfClOzXWcnYRqci\r\n"
            "Content-Disposition: form-data; name=\"request_submit[occupationMode]\"\r\n\r\n"
            "alone\r\n"
            "------WebKitFormBoundaryIjfClOzXWcnYRqci\r\n"
            f"Content-Disposition: form-data; name=\"accommodation\"\r\n\r\n"
            f"{accommodation_id}\r\n"
            "------WebKitFormBoundaryIjfClOzXWcnYRqci--\r\n"
        )
        
        async with session.post(url, data=data) as response:
            if response.status == 200:
                print(await response.text())
                print(await response.json())
                print("booked")
                
            else:
                print("error while booking", await response.json())


import asyncio

async def main():
    
    async with CrousSession(36) as crous:
        # await crous.add_accommodation_to_selection(478)
        await crous.book_accommodation(980)
        # await test()
    
asyncio.run(main())

