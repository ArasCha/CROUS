from msg import *
from req import get_data, get_data_simulation, TokenDead, request
import re
import json
import traceback


wish = {
    "bedCount": 1
}

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
        
        filtered_data = filter(is_wished, data)
        await make_msg(data)

    except TokenDead:
        await tell_no_token()
        return
    except Exception as error:
        error_traceback = traceback.format_exc()
        await tell_error(error_traceback)


def is_wished(acc:dict) -> bool:
    """
    Filter accomodations that aren't relevant to wishes
    acc: Data of an accomodation
    """

    for wish in wishes:
        if wish["bedCount"] == acc["bedCount"]:
            # if re.search(wish["residence"], acc["residence"]["label"], re.IGNORECASE):
                return True
    return False



async def is_token_ok(token:str) -> bool:

    try:
        await get_data([api_versions[0]], token=token)
    except TokenDead:
        return False
    return True
