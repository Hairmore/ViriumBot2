from tkinter import ROUND
import pandas as pd
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from typing import Optional
import os
import numpy as np
import re

THRESHOLD_SCORE = 25
WHITELIST_ROUND = 4 
SERVER_ID =923145834890145802
TICKET_ADMIN_ROLE_ID = 935826124368404500 #Admins have the right to start a new round
WHITELIST_CHANNEL = 940756444486205490
WHITELIST_WINNER_ROLE_ID = 946544609511735336
bot_token = os.environ['CALCU_TOKEN']


intents = discord.Intents.default()
intents.members = True
com = commands.AutoShardedBot(command_prefix="v.", intents=intents)
slash = SlashCommand(com, sync_commands=True)

csv_file = os.getcwd() + '/database.csv'#To store info for calculating

score_data = pd.DataFrame(columns = ["mem_id", "mem_name", "roles", "eventEngageTimes", "botUseTimes", "spamTimes", "MisbehaviorTimes", "Invites", "Followed", "InfluencerFollower", "FUD", "BadSub", "spamRepo", "score"])
if not os.path.exists(csv_file):
    score_data.to_csv(csv_file, index=False, sep="\t")

@slash.slash(
    name = "whitelist_number",
    description = "Launch when a new round is started",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "number",
            description = "Set the number of whitelist to hand out",
            required=True,
            option_type = 4 #type 6 is USER
            ),
        create_option(
            name = "round",
            description = "Set the number of whitelist to hand out",
            required=True,
            option_type = 4 #type 6 is USER
            )
        ]
    )
@commands.has_role(TICKET_ADMIN_ROLE_ID)
async def round_start(context, number:int, round:int):
    global num_quota, counter, this_round
    num_quota = number
    this_round = round
    counter = 0
    old_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    print(old_data)
    #existing_data = old_data[-old_data['roles'].isin(["946544609511735336"])]
    #print(existing_data)
    await context.send(f'We will give {num_quota} whitelists in round {this_round}')


@com.command()
async def SCORE(cmd):
    global counter, num_quota, this_round
    # Get round num through history in whitelist channeL
    if counter < num_quota:
        try:
            print(counter, num_quota)
        except NameError:
            await cmd.send(f"{cmd.guild.get_role(TICKET_ADMIN_ROLE_ID).mention}, Please inform the bot how many whitelist will be given with command `/whitelist_number`.")
        ##########################
        members = cmd.guild.members
        """Count how many invites the command giver has"""
        csv_invite = pd.read_csv(
            os.getcwd() + '/database_inviter.csv', 
            sep="\t",
            dtype = {'user_id': str,'inviter_id':str}
        ) 
        try:
            invite_times = csv_invite['inviter_id'].value_counts()[str(cmd.author.id)]
        except KeyError:
            invite_times = 0
        """Compare it with existing data"""
        existing_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
        existing_ids = [id for id in existing_data["mem_id"].tolist()]
        for member in members:
            if not member.bot:
                team_role = [936964587717263400, 935826124368404500, 947164819927236648, 935827096373186630]#origine admin senior junior
                roles = [r.id for r in member.roles]
                inter_set = list(set(team_role)&set(roles))
                if len(inter_set) == 0:
                    dic_data = {}
                    if str(member.id) not in existing_ids:
                        #If someone new enters our server
                        dic_data["mem_id"] = str(member.id)
                        dic_data["mem_name"] = member.name
                        dic_data["roles"] = [str(role.id) for role in member.roles]
                        dic_data["eventEngageTimes"] = 0
                        dic_data["botUseTimes"] = 0
                        dic_data["spamTimes"] = 0
                        dic_data["MisbehaviorTimes"] = 0
                        dic_data["Invites"] = invite_times
                        dic_data["Followed"] = "No"
                        dic_data["InfluencerFollower"] = 0
                        dic_data["FUD"] = 0              
                        dic_data["BadSub"] = 0    
                        dic_data["spamRepo"] = 0               
                        dic_data["score"] = 0
                        existing_data = existing_data.append([dic_data], ignore_index=True)
                    else:
                        #We update current info
                        index_ = existing_ids.index(str(member.id))
                        existing_data.iloc[index_, 2] = str(list([role.id for role in member.roles]))
                        existing_data.iloc[index_, 7] = invite_times

        existing_data.to_csv(csv_file, index=False, sep='\t')
            
        updated_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
        for index, row in updated_data.iterrows():
            #Calculation based on role names
            role_name = row["roles"]
            score = 0
            if "936964587717263400" in role_name:
                """OG"""
                score += 10
            if "943990732342067281" in role_name:
                """LEVEL 10"""
                score += 10
            if "943990968020004924" in role_name:
                """LEVEL 15"""
                score += 15
            if "943991189936406589" in role_name:
                """LEVEL 25"""
                score += 25
            if "947631016175075360" in role_name:
                """community star"""
                score += 5
            if "947630666965741599" in role_name:
                "Insightful holder"
                score += 5
            if "943652898200518666" in role_name:
                """Crypto whale"""
                score += 10
            if "943514565289861132" in role_name:
                """CRYPTO Collector"""
                score += 5
            if "947630139167088661" in role_name:
                """Contest Winner"""
                score += 10
            if "947837103092424754" in role_name:
                """Event Winner"""
                score += 10
            if "947341631605047357" in role_name:
                score += 2
            if "950764055155576882" in role_name:
                """ins follower"""
                score += 0.5
            if "947313068185116682" in role_name:
                """twitter follower"""
                score += 0.5
            #Calculation based on invite
            invit = row['Invites']
            score += invit//5 #Every 5 invites gets 1p
            #For influencer
            follower_num = row["InfluencerFollower"]
            score += follower_num
            #Contest and event engagement
            CE = row["eventEngageTimes"]
            score += CE
            #spam reporter
            sr = row["spamRepo"]
            score += sr*0.5
            ################################### Panishment #################################
            #For spam
            spam = row["spamTimes"]
            score -= spam
            #For bot use
            bot = row["botUseTimes"]
            score -= bot*5
            #For Misbehavior
            misb = row["MisbehaviorTimes"]
            score -= misb*5
            #For FUD
            fud = row["FUD"]
            score -= fud*10
            #For badSub
            badSub = row["BadSub"]
            score -= badSub*5

            """Update score"""
            updated_data.iloc[index, 13] = score

            #Give role whitelist if they have 25 points
            if counter <=num_quota:
                if score >= THRESHOLD_SCORE:
                    if "946544609511735336" not in role_name:
                        """Whitelist winner"""
                        var = cmd.guild.get_role(WHITELIST_WINNER_ROLE_ID)
                        winner = cmd.guild.get_member(int(row["mem_id"]))
                        await winner.add_roles(var)
                        #updated_data.iloc[index, 14] = this_round #更新轮数
                        counter+=1

        updated_data.to_csv(csv_file, index=False, sep='\t')      
    
    else:
        await cmd.send(f"Whitelist round {this_round} ended.")
        updated_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    
    """Sort by score"""
    tobeRank_data = updated_data[~ updated_data['roles'].str.contains(["946544609511735336"])]
    await cmd.send(tobeRank_data)
    await cmd.send(tobeRank_data['roles'])
    tobeRank_data["ranks"] = tobeRank_data["score"].rank(method="min", ascending=False) #adding a new column "rank" to dataframe

    author_index = tobeRank_data[tobeRank_data.mem_id == str(cmd.author.id)].index.tolist()[0]
    rank = tobeRank_data.iloc[author_index, 14]
    score_author = tobeRank_data.iloc[author_index, 13]
    if rank == 1:
        result = "Congrats {0}! Your score is {1}, and your rank is {2}🥇.".format(str(cmd.author).split("#")[0], str(score_author), str(int(rank)))
    elif rank == 2:
        result = "Congrats {0}! Your score is {1}, and your rank is {2}🥈.".format(str(cmd.author).split("#")[0], str(score_author), str(int(rank)))
    elif rank == 3:
        result = "Congrats {0}! Your score is {1}, and your rank is {2}🥉.".format(str(cmd.author).split("#")[0], str(score_author), str(int(rank)))
    else:
        result = "Congrats {0}! Your score is {1}, and your rank is {2}🏅.".format(str(cmd.author).split("#")[0], str(score_author), str(int(rank)))

    embedVar = discord.Embed(title="🎖 WHITELIST SCORE 🎖", description=result, color=0xD7BA99)
    embedVar.set_author(name=cmd.author.display_name,  icon_url=cmd.author.avatar_url)
    embedVar.set_image(url="https://d1fmx1rbmqrxrr.cloudfront.net/cnet/optim/i/edit/2021/12/NFT-tout-savoir-big__w770.jpg")

    await cmd.send(embed=embedVar)
    

#v:
com.run(bot_token)
