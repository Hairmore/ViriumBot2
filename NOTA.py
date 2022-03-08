from datetime import datetime
from distutils import command
import discord
from discord.ext import commands
import os
import pandas as pd
import uuid


bot_token = os.environ['NOTA']
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="/", case_insensitive=True)


#v:
MODSENIOR_ROLE_ID = 947164819927236648
MODJUNIOR_ROLE_ID = 935827096373186630
#DATABASE: 
#Command type of mod: slash command; v.SCORE, v.sendticket, v.up
# ID, Mod_name; Mod_id, Command_time, Command_message, channel_name, user_name/user_id
csv_file = os.getcwd() + '/mod_command.csv'

@client.event
async def on_message(message):
    if not os.path.exists(csv_file):
        df_mo= pd.DataFrame(columns = ["ID", "Mod_name", "Mod_id", "user_name", "user_id", "Channel_id", "Channel_name", "Command_time", "reason"])
        df_mo.to_csv(csv_file, index=False, sep='\t')
        
    mod_j= message.guild.get_role(role_id=MODJUNIOR_ROLE_ID)
    mod_s = message.guild.get_role(role_id=MODSENIOR_ROLE_ID)
    #if the message is send by a mod 
    if mod_j in message.author.roles or mod_s in message.author.roles:
        #if the message is "v.approved"
        if message.content.startswith('v.approved'):
            #Message channel
            channel_sent = message.channel
            channel_name = channel_sent.name
            channel_id = channel_sent.id
            reason = channel_sent.category.name #category name is the reason 
            existing_data_df = pd.read_csv(csv_file, sep="\t",  dtype = {'ID': str, 'Mod_id': str, "Channel_id": str, "user_id": str}, parse_dates=True)

            #message history
            msg = await channel_sent.history().flatten()
            try:
                user_name = list(set([m.author.name for m in msg if not m.author.bot and m.author != message.author]))[0]
                user_id = list(set([m.author.id for m in msg if not m.author.bot and m.author != message.author]))[0]
            except IndexError:
                user_name = None
                user_id = None
            
            #存储信息
            c_mod = {}
            c_mod['ID'] = str(uuid.uuid4())#ID
            c_mod["Mod_name"] = message.author.name
            c_mod['Mod_id'] = str(message.author.id)
            c_mod['user_name'] = user_name
            c_mod['user_id'] = user_id
            c_mod['Channel_id'] = str(channel_id)
            c_mod['Channel_name'] = str(channel_name)
            c_mod['Command_time'] = message.created_at
            c_mod["reason"] = reason #Which contest
            existing_data_df = existing_data_df.append([c_mod], ignore_index=True)
            existing_data_df.to_csv(csv_file, index=False, sep='\t')


#v:
client.run(bot_token)





            
