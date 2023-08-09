from msg import *
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

api_versions = [31]


async def prg() -> None:

    try:
        data = await get_data(api_versions)
        
        with open("../available.json", "w", encoding="utf-8") as f:
            new_data = json.dumps(data)
            f.write(new_data)
        
        filtered_data = list(filter(is_wished, data))
        await make_msg(filtered_data)

    except TokenDead:
        await tell_no_token()
        return
    except Exception as error:
        await tell_error(error)



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
