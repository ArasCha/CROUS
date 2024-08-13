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
            
            listable_acc = list(filter(is_listable, free_acc))
            if not listable_acc: return #empty
            
            cart = await crous.get_cart()
            cart_acc_ids = [acc["accommodation"]["id"] for acc in cart]
            
            listable_acc_filtered = list(filter(lambda acc: acc["id"] not in cart_acc_ids, listable_acc))
            
            for acc in listable_acc_filtered:
                
                await crous._add_accommodation_to_selection(acc["id"])
                await tell_accommodation_listed(acc)

                if is_bookable(acc):
                    await crous.book_accommodation(acc["id"])
                    await tell_accommodation_booked(acc)

        except TokenDead:
            await tell_no_token()
        except Exception as error:
            error_traceback = traceback.format_exc()
            await tell_error(error_traceback)


async def is_token_ok(token:str) -> bool:
    async with CrousSession(36) as crous:
        return await crous.test_token(token)


def is_bookable(accommodation: dict) -> list:
    
    pattern = re.compile(r"\b75\d{3}\b")
    address = accommodation["residence"]["address"]
    
    return pattern.search(address)

def is_listable(accommodation: dict) -> list:
    
    pattern = re.compile(r"\b(75|92|93|94)\d{3}\b")
    address = accommodation["residence"]["address"]

    return pattern.search(address)
