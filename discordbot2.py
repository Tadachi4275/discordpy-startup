import discord
from discord.ext import commands
import os
import traceback
import asyncio
import datetime as dt

token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix='.')



@client.event
async def on_ready() :
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def rect(ctx, about = "募集", settime = '2030-11-2,22:07:00') :
    cnt = 0
    datetime_UTC = dt.datetime.strptime(settime, '%Y-%m-%d,%H:%M:%S')
    nowTime_UTC = dt.datetime.now()
    nowTime_UTC = nowTime_UTC.replace(microsecond=0)
    td = datetime_UTC - nowTime_UTC
    print('Start Time: {0}\n'.format(nowTime_UTC))
    print('DeadLine: {0}\n'.format(datetime_UTC))
    td = float(td.seconds)
    print('Time Difference(initial)={0}(sec)\n'.format(td))
    reaction_member = [">>>"]
    test = discord.Embed(title=about, colour=0x1e90ff)
    test.add_field(name=f"{datetime_UTC}まで募集中。今{cnt}人。\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    #await ctx.send(type(msg))

    #投票の欄
    await msg.add_reaction('⏫')
    await msg.add_reaction('✖')
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⏫' or emoji == '✖'

    while 1:
        try:
            nowTime_Poll = dt.datetime.now()
            print(nowTime_Poll)
            print('Time Difference(Polling)={0}(sec)\n'.format(td))
            reaction, user = await client.wait_for('reaction_add', timeout=td, check=check)
        except asyncio.TimeoutError:
            nowTime_Det = dt.datetime.now()
            print(nowTime_Det)
            await ctx.send('締め切りｳｪｰｲ!!!!')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⏫':
                reaction_member.append(user.name)
                cnt += 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"{datetime_UTC}まで募集中。今{cnt}人。\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)
                
            elif str(reaction.emoji) == '✖':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt -= 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"{datetime_UTC}まで募集中。今{cnt}人。\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)


client.run(token)

