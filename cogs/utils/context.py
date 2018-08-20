from discord.ext import commands
import discord
import logging
import datetime
import time
logger = logging.getLogger()

class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def sad(self):
        return "<:sad:358411807460687872>"
    def happy(self):
        return "<:happy:358410748185018368>"


    @property
    def session(self):
        return self.bot.session