import discord
from discord.ext import commands
import typing
import random
import asyncio

TOKEN = 'NzMzODQ2MTA4Nzc4MDA0NTEz.XxJF_g.c7peiu2pOWE2noafWClz2KpvAjI'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def join(ctx):
    """Joins Channel."""
    global voice
    channel = ctx.author.voice.channel
    voice = await channel.connect()

@bot.command()
async def leave(ctx):
    """Leaves Channel."""
    await ctx.voice_client.disconnect()

@bot.command(name='Naughty')
async def naughty(ctx, members : commands.Greedy[discord.Member], mute_minutes: typing.Optional[int] = 0):
    """!Naughty NAME MINUTES"""

    # Get Master Role from Guild
    master_role = discord.utils.find(lambda r: r.name == '@Master', ctx.guild.roles)
    # Checks to see if author is Master
    if master_role not in ctx.author.roles:
        await ctx.send("YOU ARE NOT MASTER!")
    else:
        # If there are no members listed.
        if not members:
            await ctx.send("No one will be Punished.")
            return

        # Get Naughty Role
        naughty_role = discord.utils.find(lambda x : x.name == "The Naughty", ctx.guild.roles)

        # Punish every member listed
        for member in members:
            if master_role in member.roles: # If Master is in listed names, Skip
                embed = discord.Embed(title = "Master can never be punished.")
                await ctx.send(embed = embed)
                continue
            if bot.user == member: # Bot cannot be punished
                embed = discord.Embed(title = "PunishBOT finds the Naughty.")
                await ctx.send(embed = embed)
                continue
            await member.add_roles(naughty_role)
            await ctx.send('{} HAVE BEEN NAUGHTY AND NEEDS TIMEOUT FOR {} MINUTES'.format(member.name, str(mute_minutes)))

        if mute_minutes > 0:
            await asyncio.sleep(mute_minutes * 60)
            for member in members:
                if master_role in member.roles:
                    continue
                if bot.user == member:
                    continue
                await member.remove_roles(naughty_role, reason = "has learned their lesson.")
                #await member.edit(mute=False)
                await ctx.send('Has {} learned their lesson? Respect Master!'.format(member.name))

        # Possibly move them to different channel? Lock them from every other channel?
        #channel = discord.utils.find(lambda x : x.name == 'Naughty Room', ctx.message.guild.channels)
        #await naughty_is.move_to(channel, reason=None)
        #await naughty_is.edit(mute=True)
    
bot.run(TOKEN)