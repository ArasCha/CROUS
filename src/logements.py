from msg import *
from req import get_data, get_data_simulation, TokenDead, request
import re
import json


wishes = [
{
    "city": "Nantes",
    "max_price": 30000, # 30000 means actually 300,00€
    "min_area": 9,
    "bedCount": 1,
    "residence": "Chanzy"
}
]

async def prg() -> None:

        try:
            data = await get_data()
        except TokenDead:
            await tell_no_token()
            return

        with open("../available.json", "w", encoding="utf-8") as f:
            new_data = json.dumps(data)
            f.write(new_data)
        
        filtered_data = filter_data(data)

        await make_msg(filtered_data)



def filter_data(data:list[dict]) -> list[dict]: # keeps only wished accomodations

    filtered = []

    for wish in wishes:

        for acc in data:
            if re.search(wish["residence"], acc["residence"]["label"], re.IGNORECASE):
                filtered.append(acc)
    
    return filtered


async def is_token_ok(token:str) -> bool:

    try:
        await request(token, 27)
    except TokenDead:
        return False
    return True