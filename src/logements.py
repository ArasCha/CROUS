# from msg import *
from req import get_data, get_data_simulation, TokenDead, request
import re
import json


wishes = [
{
    "city": "Nantes",
    "residence": "Chanzy"
},
{
    "city": "Nantes",
    "residence": "Bourgeonnière"
},
{
    "city": "Nantes",
    "residence": "FRESCHE"
}
]

api_versions = [36]
"""
api_version: 27 means year 2022-2023 and 31 year 2023-2024 (32 is 2023-2024 but for the civil year 2024)
page: sometimes there are more free accomodations than what it is possible to display on one page, so many pages are needed. While our current page is not empty, we request the next page.
36 for 2024-2025
"""


async def prg() -> None:

    try:
        data = await get_data(api_versions)
        
        with open("../available.json", "w", encoding="utf-8") as f:
            new_data = json.dumps(data)
            f.write(new_data)
        
        filtered_data = list(filter(is_wished, data))
        # await make_msg(filtered_data)
        print("logements voulus libres:", filtered_data)

    except TokenDead:
        # await tell_no_token()
        print("TOKEN DEAD")
        return
    except Exception as error:
        # await tell_error(error)
        print("ERREUR:", error)



def is_wished(acc:dict) -> bool:
    """
    Filter accomodations that aren't relevant to wishes
    acc: Data of an accomodation
    """

    for wish in wishes:
        if re.search(wish["city"], acc["residence"]["sector"]["label"]):
            if re.search(wish["residence"], acc["residence"]["label"], re.IGNORECASE):
                return True
    return False



async def is_token_ok(token:str) -> bool:

    try:
        await get_data([api_versions[0]], token=token)
    except TokenDead:
        return False
    return True


import asyncio

async def main():
    
    while True:
        await prg()
        print("FINIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())