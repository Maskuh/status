import discord
from discord import app_commands
from discord.ext import commands
import datetime
import psutil
import aiohttp

# local imports

import utilities.data as data

class misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.meta = data.Meta()

    @app_commands.command(name="ping",description="Checks the latency between our servers and discords")
    async def ping(self, interaction : discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="invite",description="Sends the invite link for the bot")
    async def invite(self, interaction : discord.Interaction):
        try:
            await interaction.user.send(f"Hey there {interaction.user.mention}. Here is the invite link you asked for: https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=380105055296&scope=bot%20applications.commands")
            await interaction.response.send_message("I have sent you a DM with the invite link", ephemeral=True)
        except:
            await interaction.user.send(f"Hi {interaction.user.mention}, I am sorry but I cannot send you a DM. Please enable DMs from server members to use this command")

    @app_commands.command(name="info",description="Sends information about the bot")
    async def info(self, interaction : discord.Interaction):
        embed = discord.Embed(title="Status Checker", description="A bot that will notify you when your application goes offline", color=discord.Color.green())
        embed.set_author(name="Concept by Sambot", url="https://github.com/wotanut", icon_url="https://cdn.discordapp.com/avatars/705798778472366131/3dd73a994932174dadc65ff22b1ceb60.webp?size=2048")
        embed.add_field(name="What is this?", value="Status Checker is an open source bot that notifies you when your application goes offline or becomes unresponsive.")
        embed.add_field(name="How do I use it?", value="Each user has an \"account\" on the bot. For each user they can subscribe to an application and can send notifications to themselves or to a discord guild if they have manage server permissions in that guild. To subscribe to an application run `/subscribe` and to unsubscribe run `/unsubscribe`")
        embed.add_field(name="Sounds cool, you mentioned open source, how can I contribute?", value="First of all, thanks for your interest in contributing to this project. You can check out the source code on [GitHub](https://github.com/wotanut) where there is a more detailed contributing guide :)")
        embed.add_field(name="HELPPP", value="If you need help you can join the [Support Server](https://discord.gg/2w5KSXjhGe)")
        embed.add_field(name="I have a suggestion / bug to report", value="You can join the [Support Server](https://discord.gg/2w5KSXjhGe) and report it there or on the issues tab on [GitHub](https://github.com/wotanut/status)")
        embed.add_field(name="How can I support this project?", value="Thanks for your interest in supporting this project. You can support this project by tipping me on [Ko-Fi](https://ko-fi.com/wotanut) or by starring the [GitHub repository](https://github.com/wotanut). Furthermore, joining the [Discord Server](https://discord.gg/2w5KSXjhGe) is a great way to support the project as well as getting help with the bot")
        embed.set_footer(text="Made with ❤️ by Sambot")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="github", description="Sends the github link for the bot")
    async def github(self, interaction):
        await interaction.response.send_message("https://github.com/wotanut/status")

    @app_commands.command(name="debug", description="Sends debug information for the bot")
    async def debug(self, interaction : discord.Interaction):

        uptime = datetime.datetime.now() - self.meta.start_time

        if uptime.days > 0:
            uptime_str = f"{uptime.days} days, {uptime.seconds // 3600} hours, {uptime.seconds // 60 % 60} minutes, {uptime.seconds % 60} seconds"
        elif uptime.seconds // 3600 > 0:
            uptime_str = f"{uptime.seconds // 3600} hours, {uptime.seconds // 60 % 60} minutes, {uptime.seconds % 60} seconds"
        elif uptime.seconds // 60 % 60 > 0:
            uptime_str = f"{uptime.seconds // 60 % 60} minutes, {uptime.seconds % 60} seconds"
        else:
            uptime_str = f"{uptime.seconds % 60} seconds"


        embed = discord.Embed(title="Debug Information", description="Debug information for the bot", color=discord.Color.blue())
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Bot Uptime", value=f"{uptime_str}")
        embed.add_field(name="Bot Version", value=f"{self.meta.version} - {self.meta.version_name}")
        embed.add_field(name="Bot Memory Usage", value=f"{round(psutil.Process().memory_info().rss / 1024 ** 2)} MB")
        embed.add_field(name="Bot CPU Usage", value=f"{round(psutil.cpu_percent())}%")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="status",description="Check the status of a service")
    @app_commands.rename(bt = "bot")
    @app_commands.describe(bt = "The bot to check the status of")
    @app_commands.describe(service = "The service to check the status of")
    async def status(self, interaction : discord.Interaction, service:str = None, bt:discord.Member = None):
        if service == None and bt == None:
            await interaction.response.send_message("Please provide a service or a bot to check the status of.")
            return
        if service != None and bt != None:
            await interaction.response.send_message("You can only check the status of a bot or a service, not both.")
            return
        if service != None:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url=service) as r:
                        await interaction.response.send_message(f"Service {service} responded with status code {r.status}")
                except Exception as e:
                    await interaction.response.send_message(f"Unable to get service {service}, are you sure it is a valid URL? \n \n Error: || {e} || ")
        if bt != None:
            if bt.bot == False:
                await interaction.response.send_message("For privacy reasons, you can only check the status of bots.")
                return
            try:
                userstatus = interaction.guild.get_member(bt.id).status
                if userstatus == discord.Status.online:
                    await interaction.response.send_message(f"<:online:949589635061915648> Bot {bt.mention} is online")
                elif userstatus == discord.Status.idle:
                    await interaction.response.send_message(f"<:idle:949589635087081503> Bot {bt.mention} is idle")
                elif userstatus == discord.Status.dnd:
                    await interaction.response.send_message(f"<:dnd:949589635091284019> Bot {bt.mention} is dnd")
                else:
                    await interaction.response.send_message(f"<:offline:949589634898350101> Bot {bt.mention} is offline")
            except Exception as e:
                await interaction.response.send_message(f"Unable to get bot {bt.name}, are you sure it is a valid bot? \n \n Error: || {e} || ")



async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(misc(bot))