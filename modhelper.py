from distutils import command
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from typing import Optional
import os
import pandas as pd
import uuid

THRESHOLD_SCORE = 10
NUM_QUOTA = 2
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="", intents=intents)
slash = SlashCommand(client, sync_commands=True)
allowed_mentions = discord.AllowedMentions(everyone = True)
bot_token = os.environ['MOD_HELPER']


#v:
SERVER_ID =923145834890145802
TICKET_MOD_ROLE_ID = 935827096373186630
SENIOR_MOD_ROLE_ID = 947164819927236648


csv_file = os.getcwd() + '/database.csv'
csv_monitor = os.getcwd() + '/mod_command.csv'
if not os.path.exists(csv_monitor):
    df_mo= pd.DataFrame(columns = ["ID", "Mod_name", "Mod_id", "user_name", "user_id", "Channel_id", "Channel_name", "Command_time", "reason"])
    df_mo.to_csv(csv_monitor, index=False, sep='\t')

#ID, Mod_name; Mod_id, Command_time, Command_message, reason, user_name
##################################################### Followers ##################################################### 
@slash.slash(
    name = "Follower",
    description = "record how many follower an influencer has",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "social_media_is",
            description = "Select which social media account the member follows",
            required = True,
            option_type = 3, #type is str
            choices=[
                create_choice(
                    name = "ins",
                    value = "ins"
                ),
                create_choice(
                    name = "twitter",
                    value = "twitter"
                )
            ]
        )
        ]
    )
@commands.has_role(SENIOR_MOD_ROLE_ID)
async def follower(context, user:Optional[discord.Member], social_media_is):
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
    
    """CHANGE no to yes; add corresponding role"""
    #change no to yes
    f_df = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    index_follower = f_df[f_df.mem_id == str(user.id)].index.tolist()[0]
    if f_df.iloc[index_follower, 8] != "yes":
        f_df.iloc[index_follower, 8] = "yes"
    f_df.to_csv(csv_file, index=False, sep="\t")
    #give role
    roles_not_modBot = [r.id for r in user.roles]
    if social_media_is == "ins":
        if 950764055155576882 not in roles_not_modBot:
            var = context.guild.get_role(950764055155576882)
            await user.add_roles(var)
            m = await context.send(f'{var.name} is attached to your account now, 0.5 point will be added :).')
        else: 
            await context.send(f"{user.mention}You've already followed us on Ins")
    if social_media_is == "twitter":
        if 947313068185116682 not in roles_not_modBot:
            var = context.guild.get_role(947313068185116682)
            await user.add_roles(var)
            m = await context.send(f'{var.name} is attached to your account now, 0.5 point will be added :).')
        else: 
            await context.send(f"{user.mention}You've already followed us on Twitter")

    
    c_mod = {}
    c_mod['ID'] = str(uuid.uuid4())#ID
    c_mod["Mod_name"] = context.author
    c_mod['Mod_id'] = str(context.author.id)
    c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
    c_mod['user_id'] = str(context.kwargs['user'].id)
    c_mod['Channel_id'] = str(context.channel.id)
    c_mod['Channel_name'] = context.channel.name
    c_mod['Command_time'] = m.created_at
    c_mod["reason"] = "Follower verification: " + str(context.kwargs['user'].id) + "-" + "followed " + social_media_is
    
    existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
    existing_data_df.to_csv(csv_monitor, index=False, sep='\t')
    
##################################################### Influencer ##################################################### 

@slash.slash(
    name = "Influencer",
    description = "record how many follower an influencer has",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "social_media_accounts",
            description = "send the inluencer's social media account",
            required = True,
            option_type = 3 #type is str
        ),
        create_option(
            name = "follower_number",
            description = "send the number of followers",
            required = True,
            option_type = 4 #type is int
        )
        ]
    )
@commands.has_role(SENIOR_MOD_ROLE_ID)
async def influencer(context, user:Optional[discord.Member], social_media_accounts:str, follower_number:int):
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
    roles_not_modBot = [r.id for r in user.roles]

    """the name of the second argument has to be identical with the value of 'name' in create_option """
    if 947341631605047357 not in roles_not_modBot:
        follower_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
        index_influencer = follower_data[follower_data.mem_id == str(user.id)].index.tolist()[0]
        follower_data.iloc[index_influencer, 9] = follower_number//5000
        follower_data.to_csv(csv_file, index=False, sep="\t")
        score_added = follower_number//5000
        
        #add role
        if follower_number >= 5000:
            var = context.guild.get_role(947341631605047357)
            await user.add_roles(var)

        m = await context.send(f'{score_added} points has been added to your whitelist score.')

        c_mod = {}
        c_mod['ID'] = str(uuid.uuid4())#ID
        c_mod["Mod_name"] = context.author
        c_mod['Mod_id'] = str(context.author.id)
        c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
        c_mod['user_id'] = str(context.kwargs['user'].id)
        c_mod['Channel_id'] = str(context.channel.id)
        c_mod['Channel_name'] = context.channel.name
        c_mod['Command_time'] = m.created_at
        c_mod["reason"] = "Influencer verification: " + str(context.kwargs['user'].id) + "-" + social_media_accounts + "-" + str(follower_number)
        
        existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
        existing_data_df.to_csv(csv_monitor, index=False, sep='\t')
    
    else:
        await context.send(f'Sorry, role "Influencer" has already been added to your account.')

##################################################### Give role ##################################################### 
@slash.slash(
    name = "give_role",
    description = "Give role to the selected user",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "role",
            description = "Select the role you want to add to the selected user",
            required = True,
            option_type = 3, #type is int
            choices=[
                create_choice(
                    name = "contest winner",
                    value = "contest winner",
                ),
                create_choice(
                    name = "Insightful holder",
                    value = "Insightful holder",
                ),
                create_choice(
                    name = "Community star",
                    value = "Community star",
                ),
                create_choice(
                    name = "Event winner",
                    value = "Event winner",
                )
            ]
        ),
        ]
    )
@commands.has_role(SENIOR_MOD_ROLE_ID)
async def giverole(context, user:Optional[discord.User], role:str):
    # Open database
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
    role_dic = {"contest winner":947630139167088661, "Insightful holder": 947630666965741599, "Community star": 947631016175075360, "Event winner":947837103092424754}
    role_id = role_dic[role]
    var = context.guild.get_role(role_id)
    await user.add_roles(var)
    m = await context.send(f'{var.name} is given to {user.name}')

    c_mod = {}
    c_mod['ID'] = str(uuid.uuid4())#ID
    c_mod["Mod_name"] = context.author
    c_mod['Mod_id'] = str(context.author.id)
    c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
    c_mod['user_id'] = str(context.kwargs['user'].id)
    c_mod['Channel_id'] = str(context.channel.id)
    c_mod['Channel_name'] = context.channel.name
    c_mod['Command_time'] = m.created_at
    c_mod["reason"] = "Give role: " + str(context.kwargs['user'].id) + "-" + var.name + "given"
    existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
    existing_data_df.to_csv(csv_monitor, index=False, sep='\t')

##################################################### spam ##################################################### 
@slash.slash(
    name = "Spam",
    description = "If one sends spams",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "spam_times",
            description = "Add 1 to record",
            required = True,
            option_type = 4, #type is int
            choices=[
                create_choice(
                    name = 1,
                    value = 1
                )
            ]
        ),
        create_option(
            name = "spam_message_id",
            description = "Add 1 to record",
            required = True,
            option_type = 3, #type is int
        )
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def spam(context, user:Optional[discord.User], spam_times:int, spam_message_id: str):
    #We get the spam message
    if spam_message_id != "DM":
        spam_mssage = await context.channel.fetch_message(spam_message_id)
        existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
        
        # If already been punished
        if spam_mssage.author.id == user.id:
            if existing_data_df['reason'].str.contains(str(spam_message_id)).any():
                await context.send("This spam has already been punished", delete_after=5.0)
            else:
                    """the name of the second argument has to be identical with the value of 'name' in create_option """
                    spam_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
                    try:
                        index_influencer = spam_data[spam_data.mem_id == str(user.id)].index.tolist()[0]
                    except IndexError:
                        await context.send(f"Something went wrong, this user (id: {user.id}) is not in our database")
                    old_spam_times = spam_data.iloc[index_influencer, 5]
                    spam_data.iloc[index_influencer, 5] = old_spam_times + spam_times
                    spam_data.to_csv(csv_file, index=False, sep="\t")
                    if spam_data.iloc[index_influencer, 5] == 1:
                        #reply the spam message, so that everyone can see
                        m = await spam_mssage.reply(content = f'{context.guild.default_role} This is a spam! Be careful {user.mention}, one more spam you will be muted!', allowed_mentions = allowed_mentions)
                    if spam_data.iloc[index_influencer, 5] > 1:
                        m = await spam_mssage.reply(content = f'@everyone This is a spam! {user.mention}, YOU ARE MUTED FOR 1 HOUR!', allowed_mentions = allowed_mentions)
                    
                    c_mod = {}
                    c_mod['ID'] = str(uuid.uuid4())#ID
                    c_mod["Mod_name"] = context.author
                    c_mod['Mod_id'] = str(context.author.id)
                    c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
                    c_mod['user_id'] = str(context.kwargs['user'].id)
                    c_mod['Channel_id'] = str(context.channel.id)
                    c_mod['Channel_name'] = context.channel.name
                    c_mod['Command_time'] = m.created_at
                    c_mod["reason"] = "Sending spam: " + str(context.kwargs['user'].id) + "-" + spam_mssage.content + "-" + str(spam_mssage.id)
                    existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
                    existing_data_df.to_csv(csv_monitor, index=False, sep='\t')

            
        else:
            await context.send(f'{context.author.mention}, you select the wrong person!')

    else:
        existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
        """the name of the second argument has to be identical with the value of 'name' in create_option """
        spam_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
        try:
            index_influencer = spam_data[spam_data.mem_id == str(user.id)].index.tolist()[0]
        except IndexError:
            await context.send(f"Something went wrong, this user (id: {user.id}) is not in our database")
        old_spam_times = spam_data.iloc[index_influencer, 5]
        spam_data.iloc[index_influencer, 5] = old_spam_times + spam_times
        spam_data.to_csv(csv_file, index=False, sep="\t")
        if spam_data.iloc[index_influencer, 5] == 1:
            #reply the spam message, so that everyone can see
            m = await context.send(content = f'{user.mention} please stop DM spams to other members, one more spam you will be muted!', allowed_mentions = allowed_mentions)
        if spam_data.iloc[index_influencer, 5] > 1:
            m = await context.send(content = f'{user.mention} please stop DM spams to other members, YOU ARE MUTED FOR 1 HOUR!', allowed_mentions = allowed_mentions)
        
        c_mod = {}
        c_mod['ID'] = str(uuid.uuid4())#ID
        c_mod["Mod_name"] = context.author
        c_mod['Mod_id'] = str(context.author.id)
        c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
        c_mod['user_id'] = str(context.kwargs['user'].id)
        c_mod['Channel_id'] = str(context.channel.id)
        c_mod['Channel_name'] = context.channel.name
        c_mod['Command_time'] = m.created_at
        c_mod["reason"] = "Sending spam: " + str(context.kwargs['user'].id) + "-" + "sending DM message"
        existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
        existing_data_df.to_csv(csv_monitor, index=False, sep='\t')


##################################################### Bot Use #####################################################
@slash.slash(
    name = "BotFighter",
    description = "If one uses bot",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "bot_use",
            description = "Add 1 to record",
            required = True,
            option_type = 4, #type is int
            choices=[
                create_choice(
                    name = 1,
                    value = 1
                )
            ]
        )
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def BotFighter(context, user:Optional[discord.User], bot_use:int):
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)

    """the name of the second argument has to be identical with the value of 'name' in create_option """
    bot_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    index_influencer = bot_data[bot_data.mem_id == str(user.id)].index.tolist()[0]
    old_bot_times = bot_data.iloc[index_influencer, 4]
    bot_data.iloc[index_influencer, 4] = old_bot_times + bot_use
    bot_data.to_csv(csv_file, index=False, sep="\t")
    
    m = await context.send(f'{user}, YOU ARE MUTED FOR 24 HOUR ! 5 POINTS ARE TAKEN FROM YOUR WHITELIST SCORE !')


    c_mod = {}
    c_mod['ID'] = str(uuid.uuid4())#ID
    c_mod["Mod_name"] = context.author
    c_mod['Mod_id'] = str(context.author.id)
    c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
    c_mod['user_id'] = str(context.kwargs['user'].id)
    c_mod['Channel_id'] = str(context.channel.id)
    c_mod['Channel_name'] = context.channel.name
    c_mod['Command_time'] = m.created_at
    c_mod["reason"] = "Using bot: " + str(context.kwargs['user'].id)
    existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
    existing_data_df.to_csv(csv_monitor, index=False, sep='\t')

##################################################### Misbehaviour #####################################################
@slash.slash(
    name = "Mischief",
    description = "If one misbehaves",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "misbehave",
            description = "Add 1 to record",
            required = True,
            option_type = 4, #type is int
            choices=[
                create_choice(
                    name = 1,
                    value = 1
                )
            ]
        ),
        create_option(
            name = "misbehave_message_id",
            description = "Reply to the misbehave message",
            required = True,
            option_type = 3, #type is int

        ),

        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def Mischief(context, user:Optional[discord.User], misbehave:int, misbehave_message_id: str):
    misbehave_mssage = await context.channel.fetch_message(misbehave_message_id)
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
    
    if misbehave_mssage.author.id == user.id:
        if existing_data_df['reason'].str.contains(str(misbehave_message_id)).any():
            await context.send("This misbehavior has already been punished", delete_after=5.0)
    
        else:
        
            """the name of the second argument has to be identical with the value of 'name' in create_option """
            misb_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
            try:
                index_influencer = misb_data[misb_data.mem_id == str(user.id)].index.tolist()[0]
            except IndexError:
                await context.send(f"Something went wrong, this user (id: {user.id}) is not in our database")
            old_bot_times = misb_data.iloc[index_influencer, 6]
            misb_data.iloc[index_influencer, 6] = old_bot_times + misbehave
            misb_data.to_csv(csv_file, index=False, sep="\t")
            m = await misbehave_mssage.reply(f'{user.mention}, YOU ARE MUTED FOR 12 HOUR FOR VIOLATING THE RULE! 5 POINTS ARE TAKEN FROM YOUR WHITELIST SCORE !')

            c_mod = {}
            c_mod['ID'] = str(uuid.uuid4())#ID
            c_mod["Mod_name"] = context.author
            c_mod['Mod_id'] = str(context.author.id)
            c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
            c_mod['user_id'] = str(context.kwargs['user'].id)
            c_mod['Channel_id'] = str(context.channel.id)
            c_mod['Channel_name'] = context.channel.name
            c_mod['Command_time'] = m.created_at
            c_mod["reason"] = "Misbehave: " + str(context.kwargs['user'].id) + "-" + misbehave_mssage.content + "-" + str(misbehave_mssage.id)
            existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
            existing_data_df.to_csv(csv_monitor, index=False, sep='\t')
        
    else:
        await context.send(f'{context.author.mention}, wrong person is selected', delete_after = 5.0)


##################################################### FUD #####################################################
@slash.slash(
    name = "fud",
    description = "If one spreads unreasonable fear, uncertainty and doubt",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "fud_times",
            description = "Add 1 to record",
            required = True,
            option_type = 4, #type is int
            choices=[
                create_choice(
                    name = 1,
                    value = 1
                )
            ]
        ),
        create_option(
            name = "fud_message_id",
            description = "Reply to the misbehave message",
            required = True,
            option_type = 3, #type is int

        ),
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def fud(context, user:Optional[discord.User], fud_times:int, fud_message_id:str):
    fud_mssage = await context.channel.fetch_message(fud_message_id)
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)
    
    if fud_mssage.author.id == user.id:
        if existing_data_df['reason'].str.contains(str(fud_message_id)).any():
            await context.send("This FUD has already been punished", delete_after=5.0)
        
        else:
            """the name of the second argument has to be identical with the value of 'name' in create_option """
            fud_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
            try:
                index_influencer = fud_data[fud_data.mem_id == str(user.id)].index.tolist()[0]
            except IndexError:
                await context.send(f"Something went wrong, this user (id: {user.id}) is not in our database")
            old_bot_times = fud_data.iloc[index_influencer, 10]
            fud_data.iloc[index_influencer, 10] = old_bot_times + fud_times
            fud_data.to_csv(csv_file, index=False, sep="\t")
            m = await fud_mssage.reply(f'{user.mention}, YOU ARE MUTED FOR 24 HOUR FOR SPREADING FEAR, UNCERTAINTY AND DOUBT! 10 POINTS ARE TAKEN FROM YOUR WHITELIST SCORE !')

            c_mod = {}
            c_mod['ID'] = str(uuid.uuid4())#ID
            c_mod["Mod_name"] = context.author
            c_mod['Mod_id'] = str(context.author.id)
            c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
            c_mod['user_id'] = str(context.kwargs['user'].id)
            c_mod['Channel_id'] = str(context.channel.id)
            c_mod['Channel_name'] = context.channel.name
            c_mod['Command_time'] = m.created_at
            c_mod["reason"] = "FUD: " + str(context.kwargs['user'].id) + "-" + fud_mssage.content + "-" + str(fud_mssage.id)
            existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
            existing_data_df.to_csv(csv_monitor, index=False, sep='\t')
    else:
        await context.send(f'{context.author.mention}, wrong person is selected', delete_after = 5.0)

##################################################### Unrelated sub #####################################################
@slash.slash(
    name = "badsub",
    description = "For unrelated submission",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            ),
        create_option(
            name = "badsub_times",
            description = "Add 1 to record",
            required = True,
            option_type = 4, #type is int
            choices=[
                create_choice(
                    name = 1,
                    value = 1
                )
            ]
        ),
        create_option(
            name = "bad_submission_message_id",
            description = "Reply to the misbehave message",
            required = True,
            option_type = 3, #type is int

        )
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def badsub(context, user:Optional[discord.User], badsub_times:int, bad_submission_message_id:str):
    bad_sub_mssage = await context.channel.fetch_message(bad_submission_message_id)
    existing_data_df = pd.read_csv(csv_monitor, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)

    if bad_sub_mssage.author.id == user.id:
        if existing_data_df['reason'].str.contains(str(bad_submission_message_id)).any():
            await context.send("This bad submission has already been punished", delete_after=5.0)

        else:
            """the name of the second argument has to be identical with the value of 'name' in create_option """
            sub_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
            try:
                index_influencer = sub_data[sub_data.mem_id == str(user.id)].index.tolist()[0]
            except IndexError:
                await context.send(f"Something went wrong, this user (id: {user.id}) is not in our database")
            old_BadSub_times = sub_data.iloc[index_influencer, 11]
            old_BadSub_times
            if old_BadSub_times < 1:
                sub_data.iloc[index_influencer, 11] = old_BadSub_times + badsub_times
                sub_data.to_csv(csv_file, index=False, sep="\t")
                await bad_sub_mssage.reply(f"{user.mention}, please don't send unrelated submission. Next, 5 points will be taken from your account.")
            if old_BadSub_times >= 1:
                sub_data.iloc[index_influencer, 11] = old_BadSub_times + badsub_times
                sub_data.to_csv(csv_file, index=False, sep="\t")
                m = await bad_sub_mssage.reply(f'Sorry {user.mention}, 5 points are taken from your whitelist score for unrelated submission.')

                c_mod = {}
                c_mod['ID'] = str(uuid.uuid4())#ID
                c_mod["Mod_name"] = context.author
                c_mod['Mod_id'] = str(context.author.id)
                c_mod['user_name'] = context.kwargs['user'].name + "#" + context.kwargs['user'].discriminator
                c_mod['user_id'] = str(context.kwargs['user'].id)
                c_mod['Channel_id'] = str(context.channel.id)
                c_mod['Channel_name'] = context.channel.name
                c_mod['Command_time'] = m.created_at
                c_mod["reason"] = "Bad submission: " + str(context.kwargs['user'].id) + "-" + bad_sub_mssage.content + "-" + str(bad_sub_mssage.id)
                existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
                existing_data_df.to_csv(csv_monitor, index=False, sep='\t')

    else:
        await context.send(f'{context.author.mention}, wrong person is selected', delete_after = 5.0)

##################################################### Get score rank #####################################################
@slash.slash(
    name = "userank",
    description = "Get single user's rank and score",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "user",
            description = "choose a user",
            required=True,
            option_type = 6 #type 6 is USER
            
            )
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def userank(cmd, user:Optional[discord.Member]):
    csv_file = os.getcwd() + '/database.csv'#To store info for calculating
    """Count how many invites the command giver has"""
    updated_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    role_ids = [r.id for r in user.roles]
    team_role = [936964587717263400, 935826124368404500, 947164819927236648, 935827096373186630]#origine admin senior junior
    inter_set = list(set(team_role)&set(role_ids))
    if len(inter_set) == 0:
        """Sort by score"""
        updated_data["ranks"] = updated_data["score"].rank(method="min", ascending=False) #adding a new column "rank" to dataframe
        try:
            author_index = updated_data[updated_data.mem_id == str(user.id)].index.tolist()[0]
        except IndexError:
            cmd.send(f'Something went wrong, {user.name} is not in our database.')
        rank = updated_data.iloc[author_index, 14]
        score_author = updated_data.iloc[author_index, 13]    
        await cmd.send(f'The score of {user.name} is {score_author}, ranks {str(int(rank))}.')
    else:
        await cmd.send('No Team Member for whitelist competition.')

##################################################### Start whitelist round #####################################################
@slash.slash(
    name = "start_whitelist_round",
    description = "Launch when a new round is started",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "round",
            description = "choose a user",
            required=True,
            option_type = 4 #type 4 is int
            )
        ]
    )
@commands.has_role(TICKET_MOD_ROLE_ID)
async def round_start(context, round:int):
    COUNTER = 0
    global NUM_QUOTA
    print("hi1")
    score_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    if COUNTER < NUM_QUOTA:
        print("hi2")
        for index, row in score_data.iterrows():
            score = row["score"]
            role_id = row["roles"]
            if score >= THRESHOLD_SCORE:
                if "946544609511735336" not in role_id:
                    """Whitelist winner"""
                    var = context.guild.get_role(946544609511735336)
                    winner = context.guild.get_member(int(row["mem_id"]))
                    print(winner)
                    await winner.add_roles(var)
                    COUNTER += 1


    influen_channel = context.guild.get_channel(947304816768581642)
    contest_channel = context.guild.get_channel(947162400589750346)
    collab = context.guild.get_channel(947523081621082212)
    report_t = context.guild.get_channel(947304816768581642)
    just_level_up = context.guild.get_channel(941798257925951488)
    rules = context.guild.get_channel(941067664179204156)
    link = context.guild.get_channel(939854436120014878)
    if round == 1:
        message = f""" 
        >>> Hello @everyone, the **FIRST** round of whitelist starts.

  To earn score for whitelist, you can:
 
        🌸 Be active and levels up  👉  send command `!rank` in channel **bot command** to check your level🥳
        🌸 Participate in our events and contests. 1 point is rewarded for every participation 👉 send ticket to us 
            {contest_channel.mention}. And if you win the contest,  ✨**you win yourself 10 points**✨
        🌸 Identify yourself through Collab.Land in {collab.mention}    
            *Detailed info to be edited*
        🌸 If you are an influencer with more than 10,000 followers on Tweet or Instagram, 
                contact through tickets 👉  {influen_channel.mention}
        🌸 Follow us on Twitter and Instagram ({link.mention}), and inform us through ticket {report_t.mention}
        🌸 Guard the safety of our community 🤜 report spam once you spot one in {report_t.mention}. We reward 0.5 point for every validated report 🎉
 
  ❌ **But misbehaviors will also be punished and points can be taken from your account.** ❌ 
 

       🚧  Spreads unreasonable fear, uncertainty, and doubt ⛔️ **10 point** taken
       🚧  Uses bots to make meaningless automatic replies. We prepared channel {just_level_up.mention} for level up, 
                please don't send meaningless messages in other channels ⛔️ **5 point** taken per bot use
       🚧  Violate our server rules 👉 check them in {rules.mention} ⛔️ **5 point** taken per violation
       🚧  Send unrelated submission ⛔️ **5 point ** taken per unrelated submission
       🚧  Send spams ⛔️ **1 point** taken per spam
        """
    else:
        dic = {2:"SECOND", 3:"THIRD", 4:"LAST"}
        times = dic[round]
        message = f""" 
        >>> Hello @everyone, the **{times}** round of whitelist starts.

  To earn score for whitelist, you can:
 
        🌸 Be active and levels up  👉  send command `!rank` in channel **bot command** to check your level 🥳
        🌸 Participate in our events and contests. 1 point is rewarded for every participation 👉 send ticket to us 
            {contest_channel.mention}. And if you win the contest,  ✨**you win yourself 10 points**✨
        🌸 Identify yourself through Collab.Land in {collab.mention}    
           *Detailed info to be edited*
        🌸 If you are an influencer with more than 10,000 followers on Tweet or Instagram, 
            contact through tickets 👉  {influen_channel.mention}
        🌸 Follow us on Twitter and Instagram ({link.mention}), and inform us through ticket {report_t.mention}
        🌸 Guard the safety of our community 🤜 report spam once you spot one in {report_t.mention}. We reward 0.5 point for every validated report 🎉
 
  ❌ **But misbehaviors will also be punished and points can be taken from your account.** ❌ 
 

       🚧  Spreads unreasonable fear, uncertainty, and doubt ⛔️ **10 point** taken
       🚧  Uses bots to make meaningless automatic replies. We prepared channel {just_level_up.mention} for level up, 
             please don't send meaningless messages in other channels ⛔️ **5 point** taken per bot use
       🚧  Violate our server rules 👉 check them in {rules.mention} ⛔️ **5 point** taken per violation
       🚧  Send unrelated submission ⛔️ **5 point ** taken per unrelated submission
       🚧  Send spams ⛔️ **1 point** taken per spam
    """


    await context.send(message)

##################################################### Collect Contest submission #####################################################
@slash.slash(
    name = "collect_contestSubmission",
    description = "Use this command at the end of a contest to collect submissions in this channel",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "channel",
            description = "Choose the contest channel",
            required=True,
            option_type = 7 #type 6 is channel
            ),

        create_option(
            name = "key_word",
            description = "Enter the special hashtag for this contest",
            required=True,
            option_type = 3 #type 3 is string
            )
        ]
    )
@commands.has_role(SENIOR_MOD_ROLE_ID)
async def collect_contestSubmission(context, channel:Optional[discord.TextChannel], key_word: str):
    sub_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    csv_invite = pd.read_csv(
        os.getcwd() + '/database_inviter.csv', 
        sep="\t",
        dtype = {'user_id': str,'inviter_id':str}
    ) 

    msg = await channel.history().flatten()
    for m in msg:
        if key_word in m.content:
            try:
                index_influencer = sub_data[sub_data.mem_id == str(m.author.id)].index.tolist()[0]
            except IndexError:
                await context.send(f"Something went wrong, this user (id: {m.author.id}) is not in our database")
                try:
                    invite_times = csv_invite['inviter_id'].value_counts()[str(m.author.id)]
                except KeyError:
                    invite_times = 0
                dic_data = {}
                dic_data["mem_id"] = str(m.author.id)
                dic_data["mem_name"] = m.author.name
                dic_data["roles"] = [str(role.id) for role in m.author.roles]
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
                sub_data = sub_data.append([dic_data], ignore_index=True)
                index_influencer = sub_data[sub_data.mem_id == str(m.author.id)].index.tolist()[0]

            old_contest_times = sub_data.iloc[index_influencer, 3]
            sub_data.iloc[index_influencer, 3] = old_contest_times + 1
            sub_data.to_csv(csv_file, index=False, sep="\t")

    await context.send("DONE")

##################################################### Event channel #####################################################
@slash.slash(
    name = "event_participation",
    description = "Use this command at the end of an event to get the name of participants",
    guild_ids = [SERVER_ID], #server id
    options = [
        create_option(
            name = "channel",
            description = "Choose the voice channel where the event is hosted",
            required=True,
            option_type = 7 #type 6 is channel
            )
        ]
    )
@commands.has_role(SENIOR_MOD_ROLE_ID)
async def event_participation(context, channel:Optional[discord.VoiceChannel]):
    #open database
    sub_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
    csv_invite = pd.read_csv(
        os.getcwd() + '/database_inviter.csv', 
        sep="\t",
        dtype = {'user_id': str,'inviter_id':str}
    ) 
    #Get members in voice channel
    members = channel.members
    for member in members:
        try:
            index_influencer = sub_data[sub_data.mem_id == str(member.id)].index.tolist()[0]
        except IndexError:
            await context.send(f"Something went wrong, this user (id: {member.id}) is not in our database")
            try:
                invite_times = csv_invite['inviter_id'].value_counts()[str(member.id)]
            except KeyError:
                invite_times = 0
            dic_data = {}
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
            sub_data = sub_data.append([dic_data], ignore_index=True)
            index_influencer = sub_data[sub_data.mem_id == str(member.id)].index.tolist()[0]

        old_contest_times = sub_data.iloc[index_influencer, 3]
        sub_data.iloc[index_influencer, 3] = old_contest_times + 1
        sub_data.to_csv(csv_file, index=False, sep="\t")

    
    await context.send("Event channel member counting done!")



client.run(bot_token)

