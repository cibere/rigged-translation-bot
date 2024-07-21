import asyncio

import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.utils import setup_logging

from bot import RiggedTranslator

setup_logging()


intents = discord.Intents.all()
bot = RiggedTranslator(commands.when_mentioned, intents=intents)


@bot.event
async def on_message(msg: discord.Message) -> None:
    if msg.author.id == bot.user.id:
        return print("Thats me")
    if not msg.content:
        return print("No content")

    embeds = []
    base_embed = discord.Embed()
    for abr, name in bot.LANGUAGES.items():
        em = base_embed.copy()
        em.title = name
        em.description = await bot.translate(msg.content, dest=abr)
        embeds.append(em)

    cap = 2000 / len(bot.LANGUAGES)
    if len(msg.content) > cap:
        msgs = {}
        for em in embeds:
            d = await msg.reply(embed=em, mention_author=False)
            msgs[em.title] = d.jump_url
        links = [f"[{lang}](<{jump}>)" for lang, jump in msgs.items()]
        await msg.reply("\n".join(links))
    else:
        await msg.reply(embeds=embeds, mention_author=False)


async def main():
    import config

    async with ClientSession() as cs:
        bot.session = cs
        await bot.start(config.token)


asyncio.run(main())
