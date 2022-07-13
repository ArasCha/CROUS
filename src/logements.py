
import time
from msg import make_msg
from req import get_data


async def prg():

    while True:

        data = get_data()
        filtered_data = filter_data(data)

        await make_msg(filtered_data)

        time.sleep(60)

def filter_data(data:list[dict]): # keeps only wished accomodations

    # filter the data
    return data
