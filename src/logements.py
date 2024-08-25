from msg import *
from req import CrousSession, ApiProblem, TokenDead
import re
import json
import traceback
from db import DB
from Accomodation import Accomodation



api_version = 36
"""
api_version: 27 means year 2022-2023 and 31 year 2023-2024 (32 is 2023-2024 but for the civil year 2024)
36 for 2024-2025
"""

async def prg() -> None:
    
    try:
        async with CrousSession(api_version) as crous:

            free_acc = await crous.get_free_accommodations()
            
            DB.set_available_accomodations(free_acc)
            accomodations = [Accomodation(acc) for acc in free_acc]
            
            listable_acc = list(filter(is_listable, accomodations))
            if not listable_acc: return #empty
            
            cart = await crous.get_cart()
            cart_acc_ids = [acc["accommodation"]["id"] for acc in cart]
            
            listable_acc_filtered = list(filter(lambda acc: acc.id not in cart_acc_ids, listable_acc))
            
            for acc in listable_acc_filtered:
                
                await crous.add_accommodation_to_selection(acc.id)
                await tell_accommodation_listed(acc)

                if is_bookable(acc):
                    await crous.book_accommodation(acc.id)
                    await tell_accommodation_booked(acc)

    except TokenDead as error:
        await tell_error(str(error))
    except ApiProblem as error:
        await tell_error(str(error))
    except Exception as error:
        error_traceback = traceback.format_exc()
        await tell_error(f"Une erreur est survenue:\n{error_traceback}")


async def is_token_ok(token:str) -> bool:
    async with CrousSession(api_version) as crous:
        return await crous.test_token(token)


def is_bookable(accommodation: Accomodation) -> list:
    
    pattern = re.compile(r"\b75005\b")
    
    return pattern.search(accommodation.address)

def is_listable(accommodation: Accomodation) -> list:
    
    pattern = re.compile(r"\b(75|92|93|94)\d{3}\b")

    return pattern.search(accommodation.address)
