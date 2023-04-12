import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()
class admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ban_guild", description="Bans a guild from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def ban_guild(self,interaction :discord.Interaction, guild:int, reason:str = None):
        try:
            guild = await self.bot.get_guild(guild)
        except Exception as e:
            await interaction.response.send_message(f"Failed to get guild, are you sure i'm in that guild? \n \n Error: || {e} ||")
        
        try:
            await guild.owner.send(f"Your guild {guild.name} has been banned from using the bot with reason {reason}. If you believe this is a mistake please contact an administrator in our discord server. https://discord.gg/2w5KSXjhGe")
        except:
            pass

        await guild.leave()

        # post it
        try:
            async with aiohttp.ClientSession() as session:
                session.post("https://api.sblue.tech/bans/guild", data={"guild_id":guild.id, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Successfully banned guild {guild.name} with reason {reason}")
        except: await interaction.reponse.send_message(f"i was unable to ban {guild.name} on the website.")
    @app_commands.command(name="unban_guild", description="Unbans a guild from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def unban_guild(self,interaction:discord.Interaction, guild:int):
        async with aiohttp.ClientSession() as session:
            try:
                session.post("https://api.sblue.tech/bans/guild/delete", data={"guild_id":guild.id, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Successfully unbanned guild {guild.name}")
            except:
                await interaction.response.send_message(f"Unable to unbann guild {guild.name}")

    @app_commands.command(name="ban_user", description="Bans a user from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def ban_user(self,interaction:discord.Interaction, user:int, reason:str = None):
        try:
            user = await self.bot.fetch_user(user)
        except Exception as e:
            await interaction.response.send_message(f"Failed to get user. \n \n Error: || {e} ||")
        
        try:
            await user.send(f"You have been banned from using the bot with reason {reason}. If you believe this is a mistake please contact an administrator in our discord server. https://discord.gg/2w5KSXjhGe")
        except:
            pass

        # post it
        async with aiohttp.ClientSession() as session:
            try:
                session.post("https://api.sblue.tech/bans/user", data={"user_id":user.id, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Banned user {user.name}#{user.discriminator} from using the bot with reason {reason}")
            except:
                await interaction.response.send_message(f"Unable to ban {user.name}#{user.discriminator}")

    @app_commands.command(name="unban_user", description="Unbans a user from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def unban_user(self,interaction:discord.Interaction, user:int):
        async with aiohttp.ClientSession() as session:
            try:
                session.post("https://api.sblue.tech/bans/user/delete", data={"user_id":user.id, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Sucesfully unbanned user {user.name}#{user.discriminator}")
            except:
                await interaction.response.send_message(f"unable to unban user {user.name}#{user.discriminator}")

    @app_commands.command(name="ban_service", description="Bans a service from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def ban_service(self,interaction:discord.Interaction, service:str, reason:str = None):
        async with aiohttp.ClientSession() as session:
            try:
                session.post("https://api.sblue.tech/bans/service", data={"service_id":service, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Successfully banned service {service} with reason {reason}")
            except:
                interaction.response.send_message(f"Unable to ban user {service}")
    @app_commands.command(name="unban_service", description="Unbans a service from using the bot")
    @app_commands.guilds(discord.Object(id=int(os.getenv("Guild"))))
    @app_commands.checks.has_role(int(os.getenv("Role")))
    async def unban_service(self,interaction:discord.Interaction, service:str):
        async with aiohttp.ClientSession() as session:
            try:
                session.post("https://api.sblue.tech/bans/service/delete", data={"service_id":service, "token":os.getenv("SBLUE_TECH_API_KEY")})
                await interaction.response.send_message(f"Successfully unbanned service {service}")
            except:
                await interaction.response.send_message(f"unable to unban user {service}")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(admin(bot))