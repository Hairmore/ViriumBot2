from curses.panel import bottom_panel
import discord
from discord.ext import commands
import DiscordUtils
import pandas as pd
import os
import numpy as np

bot_token = os.environ['INVITES_TOKEN']

intents = discord.Intents.default()
intents.members = True
com = commands.AutoShardedBot(command_prefix="", intents=intents)
tracker = DiscordUtils.InviteTracker(com)



df_invite = pd.DataFrame(columns=['user_name', 'user_id', 'inviter_name', 'inviter_id'])
csv_file = os.getcwd() + '/database_inviter.csv'
if not os.path.exists(csv_file):
    df_invite.to_csv(csv_file, index=False, sep="\t")

@com.event
async def on_member_remove(member):
    df_leave = pd.read_csv(csv_file, sep="\t", dtype = {'user_id': str,'inviter_id':str})
    leave_index = df_leave[df_leave['user_id'] == member.id].index.tolist()
    df_leave = df_leave.drop(df_leave.index[[leave_index]])
    df_leave.to_csv(csv_file, sep="\t", index=False)

 
@com.event
async def on_member_join(member):
    if not member.bot:
        inviter = await tracker.fetch_inviter(member)
        dic_inv_info = {}
        dic_inv_info['user_name'] = member.name
        dic_inv_info['user_id'] = str(member.id)
        dic_inv_info['inviter_name'] = inviter.name
        dic_inv_info['inviter_id'] = str(inviter.id)
        df_adding = pd.read_csv(csv_file, sep="\t", dtype = {'user_id': str,'inviter_id':str})
        df_adding = df_adding.append([dic_inv_info], ignore_index=True)
        df_adding.to_csv(csv_file, sep="\t", index=False)


#v:
com.run(bot_token)
