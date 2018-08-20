import discord
import datetime
import aiohttp
import asyncio
from discord.ext import commands
import config
import sys, traceback
import time
from cogs.utils import context
import logging
import os

logger = logging.getLogger()


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(current_dir, "logs")
    handler = logging.FileHandler(filename='{}/{}.log'.format(logs_dir, datetime.datetime.now().strftime('%Y-%m-%d')),
                                  encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    logger = logging.getLogger()
    logger.addHandler(handler)
    return handler


initial_extensions = [ 'cogs.al']

def _prefix_callable(bot, msg):
    return 's!'


class ArkBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=_prefix_callable, description="",
                         pm_help=None, help_attrs=dict(hidden=True))

        self.session = aiohttp.ClientSession(loop=self.loop)
        self.owner_id = 77509464290234368

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


        self.log_handler = configure_logging()
        self.awake_time = datetime.datetime.now()



    def check_logger(self):
        today = datetime.datetime.now()
        if today.year != self.awake_time.year or today.month != self.awake_time.month or today.day != self.awake_time.day:
            logger.removeHandler(self.log_handler)
            self.awake_time = today
            self.log_handler = configure_logging()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)
        else:
            print(f'{error}', file=sys.stderr)

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id})')

        try:
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game("osu!"))
        except: pass

    async def close(self):
        await super().close()
        await self.session.close()

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:
            return ctx

        self.check_logger()

        logger.info(f"Invoking command {str(ctx.command.qualified_name)}")


        await self.invoke(ctx)

        return ctx

    async def on_message(self, message):
        await self.process_commands(message)

    def run(self):
        super().run(config.token, reconnect=True)
