import dscrd

async def make_msg(accomodations: list[dict]) -> None:

    for acc in accomodations:
        area = acc["area"]["max"]
        rent = acc["occupationModes"][0]["rent"]["max"]
        residence = acc["residence"]["label"]
        id = acc["id"]
        booking_link = f"https://trouverunlogement.lescrous.fr/tools/residual/26/accommodations/{id}"

        await dscrd.notifier(f"**Nouveau Logement**:\n{residence}\n{rent/100}€/mois\n{area}m²\n{booking_link}")
