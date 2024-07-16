import dscrd

async def make_msg(accomodations: list[dict]) -> None:

    for acc in accomodations:
        area = acc["area"]["max"]
        rent = acc["occupationModes"][0]["rent"]["max"]
        residence = acc["residence"]["label"]
        id = acc["id"]
        address = acc["address"]
        booking_link = f"https://trouverunlogement.lescrous.fr/tools/36/accommodations/{id}"
        
        await dscrd.notifier(f"**Nouveau Logement**:\n{residence} - {address}\n{rent/100}€/mois\n{area}m²\n{booking_link}")

async def tell_no_token() -> None:
    await dscrd.send_msg("**Le token est mort**")

async def tell_error(error_traceback: str) -> None:
    await dscrd.send_msg(f"Une erreur est survenue:\n{error_traceback}")
