from msg import make_msg
from req import get_data

status = True

async def prg():

    data = get_data()
    filtered_data = filter_data(data)

    await make_msg(filtered_data)


def filter_data(data:list[dict]) -> list[dict]: # keeps only wished accomodations

    wish = {
        "city": "Nantes",
        "max_price": 30000,
        "min_area": 9,
        "bedCount": 1
    } # 30000 means actually 300,00€

    filtered = []

    for acc in data:
        if acc["area"]["max"] >= wish["min_area"]:
            if acc["bedCount"] == wish["bedCount"]:
                if acc["occupationModes"][0]["rent"]["max"] <= wish["max_price"]:
                    filtered.append(acc)
    
    return filtered
