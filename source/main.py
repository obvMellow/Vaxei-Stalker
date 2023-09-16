from ossapi import Ossapi
import asyncio
import discord
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open("config.json", "r") as config:
    config = json.load(config)

stalk_channel_id = config["stalk_channel_id"]
ping_id = config["ping_id"]


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    online_res = False

    while True:
        channel = client.get_channel(stalk_channel_id)
        online = is_online()

        if online and online != online_res:
            await channel.send(content="<@&1150272758350098452> Vaxei is now online!")

        online_res = online

        await asyncio.sleep(10)


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != stalk_channel_id:
        return

    if message.content == "v!check":
        online = is_online()

        if online:
            msg = "Vaxei is currently online!"
        else:
            msg = "Vaxei is currently not online."

        await message.reply(content=msg)


def is_online():
    client_id = config["client_id"]
    client_secret = config["client_secret"]

    api = Ossapi(client_id, client_secret)

    return api.user("Vaxei").is_online


client.run(config["token"])
