from msg import tell_accommodation_booked, tell_accommodation_listed, tell_error, tell_new_accommodation
from req import CrousSession, ApiProblem, TokenDead, get_data_simulation
import re
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

            notifiable_acc = list(filter(is_notifiable, accomodations))

            for acc in notifiable_acc:
                await tell_new_accommodation(acc)
            
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


def is_bookable(accommodation: Accomodation) -> bool:
    
    wishes = [
        {
            "address_pattern": re.compile(r"\b75013\b"),
            "residence_pattern": re.compile(r"Lalet", re.IGNORECASE)
        },
        {
            "address_pattern": re.compile(r"\b75005\b"),
            "residence_pattern": re.compile(r"Rollin", re.IGNORECASE)
        },
        {
            "address_pattern": re.compile(r"\b75005\b"),
            "residence_pattern": re.compile(r"Hostater", re.IGNORECASE)
        },
        {
            "address_pattern": re.compile(r"\b75006\b"),
            "residence_pattern": re.compile(r"Mazet", re.IGNORECASE)
        },
    ]
    
    for wish in wishes:
        if wish["address_pattern"].search(accommodation.address) and wish["residence_pattern"].search(accommodation.residence_name) and accommodation.min_area >= 17:
            return True

def is_listable(accommodation: Accomodation) -> bool:
    
    return is_bookable(accommodation)


def is_notifiable(accommodation: Accomodation) -> bool:
    
    wishes = [
        {
            "address_pattern": re.compile(r"\b75006\b"),
            "residence_pattern": re.compile(r"Bonaparte", re.IGNORECASE)
        },
        {
            "address_pattern": re.compile(r"\b75005\b"),
            "residence_pattern": re.compile(r"Carmes", re.IGNORECASE)
        },
        {
            "address_pattern": re.compile(r"\b75014\b"),
            "residence_pattern": re.compile(r"Jacques", re.IGNORECASE)
        }
    ]

    for wish in wishes:
        if wish["address_pattern"].search(accommodation.address) and wish["residence_pattern"].search(accommodation.residence_name):
            return True