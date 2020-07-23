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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command')

@bot.command()
async def join(ctx):
    """Joins Channel."""
    global voice
    channel = ctx.author.voice.channel
    voice = await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))

@bot.command()
@commands.has_role("@Master")
async def naughty(ctx, members : commands.Greedy[discord.Member], mute_minutes: typing.Optional[int] = 0):
    """!Naughty NAME MINUTES"""
    
    # if master_role not in ctx.author.roles:
    #     await ctx.send("YOU ARE NOT MASTER!")
    # else:
    # if not members:
    #     await ctx.send("No one will be Punished.")
    #     return

    master_role = discord.utils.find(lambda r: r.name == '@Master', ctx.guild.roles) # Master Role
    naughty_role = discord.utils.find(lambda x : x.name == "The Naughty", ctx.guild.roles) # The Naughty
    channel = discord.utils.find(lambda x : x.name == 'Naughty Room', ctx.message.guild.channels) # Naughty Room

    for member in members:
        if master_role in member.roles:
            embed = discord.Embed(title = "Master can never be punished.")
            await ctx.send(embed = embed)
            continue
        if bot.user == member:
            embed = discord.Embed(title = "PunishBOT finds the Naughty.")
            await ctx.send(embed = embed)
            continue
        await member.add_roles(naughty_role)
        await member.move_to(channel, reason=None)
        await ctx.send('{} HAS BEEN NAUGHTY AND NEEDS TIMEOUT FOR {} MINUTES'.format(member.name, str(mute_minutes)))

    dojo = discord.utils.find(lambda x : x.name == 'General', ctx.message.guild.channels)

    if mute_minutes > 0:
        await asyncio.sleep(mute_minutes * 60)
        for member in members:
            if master_role in member.roles:
                continue
            if bot.user == member:
                continue
            await member.remove_roles(naughty_role, reason = "has learned their lesson.")
            await member.move_to(dojo, reason=None)
            await ctx.send('Has {} learned their lesson? Respect Master!'.format(member.name))

@naughty.error
async def naughty_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('YOU ARE NOT MASTER!')

    if isinstance(error, commands.BadArgument):
        await ctx.send('No one will be Punished.')     

bot.run(TOKEN)