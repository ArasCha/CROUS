from msg import *
from req import get_data


wish = {
    "city": "Nantes",
    "max_price": 30000, # 30000 means actually 300,00€
    "min_area": 9,
    "bedCount": 1
}

async def prg() -> None:

    data = get_data()

    if data is None:
        await tell_no_token()
        return
    
    filtered_data = filter_data(data)

    await make_msg(filtered_data)


def filter_data(data:list[dict]) -> list[dict]: # keeps only wished accomodations

    filtered = []

    for acc in data:
        if acc["area"]["max"] >= wish["min_area"]:
            if acc["bedCount"] == wish["bedCount"]:
                if acc["occupationModes"][0]["rent"]["max"] <= wish["max_price"]:
                    filtered.append(acc)
    
    return filtered


def test_req() -> bool:

    data = get_data()

    if data is None: return False
    else: return True