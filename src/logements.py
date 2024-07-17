from msg import *
from req import get_data_simulation, TokenDead, CrousSession
import re
import json
import traceback



api_version = 36
"""
api_version: 27 means year 2022-2023 and 31 year 2023-2024 (32 is 2023-2024 but for the civil year 2024)
36 for 2024-2025
"""

async def prg() -> None:
    
    async with CrousSession(36) as crous:

        try:
            free_acc = await crous.get_free_accommodations()
            
            with open("../available.json", "w", encoding="utf-8") as f:
                new_data = json.dumps(free_acc)
                f.write(new_data)
            
            [await crous._add_accommodation_to_selection(acc["id"]) for acc in free_acc]
            [await tell_accommodation_listed(acc) for acc in free_acc]
            
            bookable_acc = list(filter(is_bookable, free_acc))
            [await crous.book_accommodation(acc["id"]) for acc in bookable_acc]
            [await tell_accommodation_booked(acc) for acc in bookable_acc]


        except TokenDead:
            await tell_no_token()
        except Exception as error:
            error_traceback = traceback.format_exc()
            await tell_error(error_traceback)


async def is_token_ok(token:str) -> bool:
    async with CrousSession(36) as crous:
        return await crous.test_token(token)


def is_bookable(accommodation: dict) -> list:
    
    post_codes = ["75005","75006"]
    address = accommodation["residence"]["address"]
    
    return any(post_code in address for post_code in post_codes)