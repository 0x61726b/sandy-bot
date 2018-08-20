import sys
import click
import logging
import asyncio
import config
import discord
import importlib
import contextlib
from bot import ArkBot, initial_extensions, configure_logging
def run_bot(**kwargs):
    loop = asyncio.get_event_loop()

    bot = ArkBot(**kwargs)
    bot.run()


@click.group(invoke_without_command=True, options_metavar='[options]')
@click.pass_context
def main(ctx):
    """Launches the bot."""
    if ctx.invoked_subcommand is None:

        # Run the bot
        options = dict()
        run_bot(**options)

if __name__ == '__main__':
    main()