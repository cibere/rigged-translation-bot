import discord
from aiohttp import ClientSession
from discord.ext import commands

import translator


class RiggedTranslator(commands.Bot):
    user: discord.ClientUser
    session: ClientSession

    LANGUAGES = {
        "es": "Spanish",
        "en": "English",
        "ja": "Japanese",
        "ru": "Russian",
        "vi": "Vietnamese",
        "ar": "Arabic",
    }

    async def translate(self, msg: str, /, dest: str) -> str:
        res = await translator.translate(msg, dest=dest, session=self.session)
        return res.translated

    async def setup_hook(self) -> None:
        for key, val in self.LANGUAGES.items():
            self.LANGUAGES[key] = await self.translate(val, dest=key)

    async def on_ready(self) -> None:
        print(f"I'm logged in as {self.user} ({self.user.id})")
