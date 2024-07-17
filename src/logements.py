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
            data = await crous.get_free_accomodations()
            
            with open("../available.json", "w", encoding="utf-8") as f:
                new_data = json.dumps(data)
                f.write(new_data)
            
            await make_msg(data)

        except TokenDead:
            await tell_no_token()
        except Exception as error:
            error_traceback = traceback.format_exc()
            await tell_error(error_traceback)


async def is_token_ok(token:str) -> bool:
    return await crous_session.test_token(token)
