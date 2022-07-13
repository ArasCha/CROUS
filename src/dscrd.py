import discord
from logements import prg
from dotenv import dotenv_values


def_int = discord.Intents.default()
def_int.members = True # nécessaire pour agir sur les membres

client = discord.Client(intents = def_int)


#-----------------------------------------------------------------------------------------


# décorateur pour les coroutines (équivalent des promesses en JS):
@client.event # Pour dire que la fonction on_ready est une fonction d'événements.
async def on_ready(): # lorsque l'on a lancé le bot par client.run()
    
    print("Programme lancé")
    await prg()


async def notifier(msg:str):

    channel: discord.TextChannel = client.get_channel(996707470556803099)
    await channel.send(msg)


async def get_previous_msgs(channel:discord.TextChannel) -> list[str]:

    messages: list[discord.Message] = await channel.history(limit=200).flatten()
    return [msg.content for msg in messages]


config = dotenv_values(".env")
client.run(config["DISCORD_BOT_TOKEN"])