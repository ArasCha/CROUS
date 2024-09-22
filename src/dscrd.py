import json
import discord
from datetime import datetime
from logements import prg, is_token_ok
from dotenv import dotenv_values, set_key
from discord.ext import commands
import asyncio
import re
import os
from db import DB


client = commands.Bot(command_prefix = '!')

#-----------------------------------------------------------------------------------------


# décorateur pour les coroutines (équivalent des promesses en JS):
@client.event # Pour dire que la fonction on_ready est une fonction d'événements.
async def on_ready() -> None: # lorsque l'on a lancé le bot par client.run()
    
    print("Bot ready")
    await send_msg("Programme démarré")

    async def loop():
        while True:
            if DB.get_program_status():
                await prg()
            await asyncio.sleep(30)
    
    prog = asyncio.create_task(loop())


#---------------------------------------COMMANDS-----------------------------------------


@client.command()
async def status(context:commands.Context) -> None:

    if DB.get_program_status():
        await context.send("Le programme est en cours de fonctionnement")
    else:
        await context.send("Le programme est arrêté")
    
    last_modification_time = DB.get_last_accomodations_update_time()
    await context.send(f"Dernière mise à jour des données: {last_modification_time}")

@client.command()
async def stop(context:commands.Context) -> None:

    if DB.get_program_status():
        DB.set_program_status(False)
        await context.send("Le programme s'arrête")
        print("Stopped")
    else:
        await context.send("Le programme est déjà arrêté")

@client.command()
async def start(context:commands.Context) -> None:

    if not DB.get_program_status():
        DB.set_program_status(True)
        await context.send("Le programme démarre")
        print("Started")
    else:
        await context.send("Le programme est déjà démarré")


@client.command()
async def token(context:commands.Context, token) -> None:

    if await is_token_ok(token):
        set_key("../.env", "CROUS_TOKEN", token)
        await context.send("Ce token fonctionne")
    else:
        await context.send("Ce token ne fonctionne pas")


@client.command()
async def city(context:commands.Context, *args) -> None: # envoie dans le tchat les logements qui correspondent à la ville demandée

    data = []
    wished_city = " ".join(args)
    
    for acc in DB.get_accomodations_from_address(wished_city):
            msg = f"{acc.address} - {acc.residence_name}\n{acc.max_rent}€/mois\n{acc.max_area}m²"
            await context.send(msg)


@client.command()
async def clear(context:commands.Context, nb) -> None: # delete the last nb messages

    messages: list[discord.Message] = await get_previous_msgs(context.channel)

    nb = int(nb)

    if nb > len(messages):
        nb = len(messages)

    for i in range(nb):
        await delete_message(messages[i])


#-------------------------------------FUNCTIONS-----------------------------------------


async def notifier(msg:str) -> None:

    channel: discord.TextChannel = client.get_channel(996707470556803099)
    await clean_old_msgs(channel)
    if not await already_sent(msg, channel):
        await send_msg(msg)

async def send_msg(msg:str) -> None:

    channel: discord.TextChannel = client.get_channel(996707470556803099)
    await channel.send(msg)

async def get_previous_msgs(channel:discord.TextChannel) -> list[str]:

    messages: list[discord.Message] = await channel.history(limit=200).flatten()
    return messages

async def delete_message(message:discord.Message):
    try:
        await message.delete()
    except discord.errors.HTTPException:
        print("discord.errors.HTTPException: currently waiting and retrying")
        await asyncio.sleep(5)
        await message.delete()

async def clean_old_msgs(channel:discord.TextChannel) -> None:

    messages: list[discord.Message] = await get_previous_msgs(channel)

    for msg in messages:
        now = datetime.now()
        one_day = datetime(2000, 1, 2, 0, 0, 0) - datetime(2000, 1, 1, 0, 0, 0)

        if now - msg.created_at > one_day:
            await delete_message(msg)


async def already_sent(msg:str, channel:discord.TextChannel) -> bool:

    messages: list[discord.Message] = await get_previous_msgs(channel)

    for message in messages:
        if message.content == msg:
            return True

    return False



config = dotenv_values("../.env")
client.run(config["DISCORD_BOT_TOKEN"])