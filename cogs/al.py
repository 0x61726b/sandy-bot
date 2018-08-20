import datetime
import discord
import logging
import asyncio
from discord.ext import commands
import os

logger = logging.getLogger()

class ALCog:
    def __init__(self, bot):
        self.bot = bot

        self.emote = "<:sandybotLUL:481182499041443863>"
        self.calculate_reset(15,24, "JP Server", "Commanders, Daily Quests/PvP/Medal Shop/Gold Shop have reset!")
        self.calculate_reset(7,24, "EN Server", "Commanders, Daily Quests/PvP/Medal Shop/Gold Shop have reset!")

        self.calculate_reset(3, 12, "JP Server",
                             "Commanders, PvP/Gold Shop have reset!")

        self.calculate_reset(19, 12, "EN Server",
                             "Commanders, PvP/Gold Shop have reset!")


        self.target_channel = 467661497833619467


    def get_time_remaining_for_task(self, server, task):
        if server == "jp":
            if task == "daily":
                reset_hour = 15
            elif task == "shop":
                reset_hour = 7
            else:
                return

        elif server == "en":
            if task == "daily":
                reset_hour = 7
            elif task == 'shop':
                reset_hour = 19
            else:
                return
        else:
            return

        if reset_hour == None:
            return None


        now = datetime.datetime.utcnow()
        daily_reset = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=reset_hour, minute=0,
                                        second=0)

        if now.hour >= reset_hour and now.minute > 0:
            daily_reset = daily_reset + datetime.timedelta(days=1)

        return (daily_reset - now).total_seconds()



    @commands.command(name='reset')
    async def cmd_reset(self, context, server:str, task:str):
        remaining_time = self.get_time_remaining_for_task(server, task)
        if remaining_time == None:
            return await context.send("Commanders, invalid parameters!")

        if task == "daily":
            message = f"Commanders, Daily Quests/PvP/Medal Shop/Gold Shop resets in {remaining_time/(60*60):0.2f} hours!"
        elif task == "shop":
            message = f"Commanders, PvP/Gold Shop resets in {remaining_time/(60*60):0.2f} hours!"
        else:
            return await context.send("Commanders, invalid parameters!")
        e = discord.Embed(title=f"{self.emote} {message}", colour=discord.Color.purple())
        if server == "en":
            server = "EN Server"
        elif server == "jp":
            server = "JP Server"
        e.set_footer(text=server)
        await context.send(embed=e)


    def calculate_reset(self, reset_hour, repeat_in_hours, server, message):
        now = datetime.datetime.utcnow()
        daily_reset = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=reset_hour, minute=0, second=0)

        if now.hour >= reset_hour and now.minute > 0:
            daily_reset = daily_reset + datetime.timedelta(days=1)

        seconds_until_reset = (daily_reset - now).total_seconds()


        print(f"{message} - {server}: {daily_reset} Hours left: {seconds_until_reset/(60*60):0.2f}")

        e = discord.Embed(title=f"{self.emote} {message}", colour=discord.Color.purple())
        e.set_footer(text=server)
        self.bot.loop.create_task(asyncio.coroutine(self.reset_task)(seconds_until_reset, repeat_in_hours * 60 * 60, e))

    async def reset_task(self, seconds_to_wait, repeat_seconds, embed):
        await self.bot.wait_until_ready()

        logger.info(f"Waiting {seconds_to_wait}.. repat in {repeat_seconds} seconds")
        await asyncio.sleep(int(seconds_to_wait))

        logger.info(f"Posting...")
        await self.bot.get_channel(self.target_channel).send(embed=embed)

        self.bot.loop.create_task(asyncio.coroutine(self.reset_task)(repeat_seconds, repeat_seconds, embed))





def setup(bot):
    bot.add_cog(ALCog(bot))
