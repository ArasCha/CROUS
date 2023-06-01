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
        
        filtered_data = list(filter(is_wished, data))

        await make_msg(filtered_data)



def is_wished(acc:dict) -> bool:
    """
    Filter accomodations that aren't relevant to wishes
    acc: Data of an accomodation
    """

    for wish in wishes:
        if re.search(wish["residence"], acc["residence"]["label"], re.IGNORECASE):
            return True
    return False



async def is_token_ok(token:str) -> bool:

    try:
        await request(token, 27)
    except TokenDead:
        return False
    return True
