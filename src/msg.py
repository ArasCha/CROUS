import dscrd

def format_acc_msg(acc) -> str:
    return f"{acc.residence_name} - {acc.address}\n{acc.max_rent}€/mois\n{acc.max_area}m²"

booking_link_basis = "https://trouverunlogement.lescrous.fr/tools/36/accommodations/"

async def tell_new_accommodation(accommodation) -> None:
    booking_link = booking_link_basis + accommodation.id
    await dscrd.notifier(f"""**Nouveau logement**:\n
                         {format_acc_msg(accommodation)}\n
                        {booking_link}""")

async def tell_accommodation_listed(accommodation) -> None:
    reservation_link = f"https://trouverunlogement.lescrous.fr/tools/36/cart"
    await dscrd.notifier(f"""**Logement ajouté à la liste**:\n
                         {format_acc_msg(accommodation)}\n
                        {reservation_link}\n
                        {booking_link_basis}{accommodation.id}""")
    
async def tell_accommodation_booked(accommodation) -> None:
    await dscrd.notifier(f"""**Logement demandé**:\n
                         {format_acc_msg(accommodation)}\n
                        {booking_link_basis}{accommodation.id}""")
    

async def tell_error(message: str) -> None:
    await dscrd.notifier(message)
