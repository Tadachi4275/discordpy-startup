import discord
from discord.ext import commands
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix='.')



@client.event
async def on_ready() :
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def rect(ctx, about = "募集", cnt = 4, settime = 10.0) :
    cnt, settime = int(cnt), float(settime)
    reaction_member = [">>>"]
    test = discord.Embed(title=about, colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人　募集中\n", value=None, inline=True)
    await ctx.send(embed=test)

    #投票の欄
    await ctx.message.add_reaction('⏫')
    await ctx.message.add_reaction('✖')

client.run(token)

