from distutils.cmd import Command
import discord
from discord.ext import commands
import datetime
from helper import Helper
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
discord.Intents.presences = True

bot = discord.Client(intents=intents)

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

class bot_info():
    def __init__(self):
        self.name = "Status Checker"
        self.id = 845943691386290198
        self.token = ""
        self.owner = "Sambot"
        self.owner_id = 705798778472366131
        self.start_time = datetime.datetime.now()

@bot.event
async def on_ready():
    # on ready we will start the web server, set the bot's status and log the uptime as well as a few other admin things
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots"))
  
    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now()}", color=0x00ff00)
    await log_channel.send(embed=embed)

    # start checking the services

@bot.event
async def on_command_error(ctx,error):
    await ctx.send(f"An error occured: {error}")

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Error", description=f"An error occured: {error} \n In Guild: {ctx.guild.name} \n Guild Owner: {ctx.guild.owner.mention}", color=0xff0000)
    await log_channel.send(embed=embed)
    
@bot.event
async def on_presence_update(before,after):
    if before.bot == True:
        return
    elif before.id == bot.user.id:
        return
    elif before.status == after.status:
        return
    elif Helper.check_database(before.id) == False:
        return

    application = Helper.get_from_database(before.id)
    if application["application_type"] != "bot":
        return # if the bot is not a bot, we will not do anything

    for notification in bot["notifications"]:
        if notification["webhook"]:
            Helper.webhook(notification["webhook"]) 
        elif notification["email"]:
            Helper.email(notification["email"])
        elif notification["sms"]:
            Helper.sms(notification["sms"])
        elif notification["discord"]:

            # send the message

            channel = await bot.get_channel(notification["discord"]["channel"])
            if notification["discord"]["content_type"] == "application/json":
                await channel.send(embed=discord.Embed.from_dict(notification["discord"]["payload"]))
            else:
                await channel.send(notification["discord"]["payload"])
            
            # auto publish
            if notification["discord"]["auto_publish"] == True:
                try:
                    await channel.publish()
                except:
                    pass
            
            # auto lock
            if notification["discord"]["auto_lock"] == True:
                guild = await bot.fetch_guild(notification["discord"]["guild"])
                try:
                    for channel in guild.channels:
                        if channel.id == notification["discord"]["channel"]:
                            await channel.edit(guild.default_role, reason="Auto locked channel", overwrites=discord.PermissionOverwrite(send_messages=False))
                except:
                    pass
        
            pass
        elif notification["dm"]:
            user = await bot.fetch_user(notification["dm"]["user"])
            if notification["dm"]["content_type"] == "application/json":
                await user.send(embed=discord.Embed.from_dict(notification["dm"]["payload"]))
            else:
                await user.send(notification["dm"]["payload"])

            pass


    raise discord.errors.ClientException()

@bot.event
async def on_guild_join(guild):
    # send a message to the channel
    try:
        guild = await bot.get_guild(guild)
        channel = await guild.get_channel()[0]
        embed = discord.Embed(title=f"Hello, {guild.name} I am Status Checker", description="I am a bot that will notify you when your application goes offline. To get started, please run the command `/setup`", color=discord.Color.green())
        await channel.send(embed=embed)
    except:
        pass
    # log the join

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="I joined a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.green())


@bot.event
async def on_guild_remove(guild):
    Helper.remove_from_database(guild.id)

    try:
        user = await bot.fetch_user(guild.owner_id)
        embed = discord.Embed(title="Hey there, I am sorry to see you go", description="All references of your guild have been removed from our database", color=discord.Color.red())

        # opportunity for a button
        await user.send(embed=embed)
    except:
        pass

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="I left a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.red())

# other commands
# ping, help, config, subscribe,unsubscribe, info, uptime<service>, status<service>,invite, dashboard,privacy

# contributor commands
# 

# administrator commands
# remove_Serivce


# aside from this we need to add commands to watch other bots stop watching other bots and view the configuration of the guild
# furthermore commands for contributors and administrators should be added too.
# web dashboard too :P



bot.run("token") # TODO: REMOVE THIS
