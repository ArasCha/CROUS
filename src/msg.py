import dscrd

def format_acc_msg(acc: dict) -> str:

    area = acc["area"]["max"]
    rent = acc["occupationModes"][0]["rent"]["max"]
    residence = acc["residence"]["label"]
    id = acc["id"]
    address = acc["residence"]["address"]
    
    return f"{residence} - {address}\n{rent/100}€/mois\n{area}m²"


async def tell_new_accommodation(accommodation) -> None:
    formatted_accommodation = format_acc_msg(accommodation)
    booking_link = f"https://trouverunlogement.lescrous.fr/tools/36/accommodations/{accommodation['id']}"
    await dscrd.notifier(f"**Nouveau logement**:\n{formatted_accommodation}\n{booking_link}")

async def tell_accommodation_listed(accommodation) -> None:
    formatted_accommodation = format_acc_msg(accommodation)
    reservation_link = f"https://trouverunlogement.lescrous.fr/tools/36/cart"
    await dscrd.notifier(f"**Logement ajouté à la liste**:\n{formatted_accommodation}\n{reservation_link}")
    
async def tell_accommodation_booked(accommodation) -> None:
    formatted_accommodation = format_acc_msg(accommodation)
    await dscrd.notifier(f"**Logement demandé**:\n{formatted_accommodation}")
    

async def tell_error(message: str) -> None:
    await dscrd.notifier(message)
