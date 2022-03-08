import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button

# discord_slash is the library I use for Button components
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    ComponentContext,
    create_actionrow,
    create_button,
)
from discord_slash.utils.manage_commands import create_choice, create_option
import pandas as pd
import os
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="v.", case_insensitive=True, help_command=None, intents = intents)
# yes it says slash, but slash commands are not used and this is required for buttons.

# Remember to edit these!
TICKET_MOD_ROLE_ID = 945043975855824977
MANAGEMENT_ROLE_ID = 946124527144927242
GUILD_ID = 945042061890039808
SLASH_BOT_ID = 946174809686016004
SERVER_ID = 945042061890039808
#Virium
MOD_S_ID = 947164819927236648
MOD_J_ID = 935827096373186630
bot_token = os.environ['APPROVO']


#DATABASE
csv_file = os.getcwd() + '/database.csv'

@client.event
async def on_ready():
    print("Bot is ready")
    global guild, ticket_modS_role, management_role, csv_file, ticket_modJ_role, test_meber # one of the annoying things about Python...

    # get the guild
    guild = client.get_guild(GUILD_ID)
    
    ticket_modS_role = guild.get_role(role_id=MOD_S_ID)  # ticket moderator role
    ticket_modJ_role = guild.get_role(role_id=MOD_J_ID)
    management_role = guild.get_role(role_id=MANAGEMENT_ROLE_ID)  # management role

@client.command(aliases=["approve"])
@commands.has_role(MOD_S_ID) 
async def approved(ctx):
    msg = await ctx.channel.history().flatten()
    author_roles = ctx.guild.get_member(ctx.author.id).roles
    message_mod = [c.content for c in msg if c.author.name == ctx.author.name][1:]
    try:
        id_not_modBot = list(set([c.author.id for c in msg if c.author.name != ctx.author.name and not c.author.bot]))[0]
    except:
        await ctx.send("Please send the command after verification.")

    roles_not_modBot = [r.name for r in ctx.guild.get_member(id_not_modBot).roles]
    #If not mod, cannot give this command
    if ticket_modS_role not in author_roles:
        if ticket_modJ_role not in author_roles:
            await ctx.send("You don't have the permission to give this command", delete_after=5.0) 
        else:
            if "v.approved" not in message_mod:
                overwrites = {
                    ctx.guild.me: discord.PermissionOverwrite(view_channel=False),
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    ticket_modS_role: discord.PermissionOverwrite(view_channel=None),
                    ticket_modS_role: discord.PermissionOverwrite(view_channel=None),
                    management_role: discord.PermissionOverwrite(view_channel=True),
                }
                await ctx.channel.edit(overwrites=overwrites)

                category_name = ctx.channel.category.name.upper()
                """
                if "FOLLOWER" in category_name:
                    if "follower" in roles_not_modBot:
                        await ctx.channel.send(f"Sorry, {ctx.guild.get_member(id_not_modBot).mention} you already identified as a follower.")
                    else:
                        await ctx.channel.send(
                            "Ticket Approved!\nYour ticket has been approved and has been transferred through to the Management Team."
                        )
                        # Once the proof is sent, we add 0.5p to the whitelist score
                        fol_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
                        author_index = fol_data[fol_data.mem_id == str(id_not_modBot)].index.tolist()[0]
                        fol_data.iloc[author_index, 8] = "Yes"
                        fol_data.to_csv(csv_file, index=False, sep='\t')

                        #We give a role to this member, and he can never open a follow ticket
                        var = discord.utils.get(ctx.guild.roles, name = "follower")
                        user = ctx.guild.get_member(id_not_modBot)
                        await user.add_roles(var)
                    """
                """
                if "CONTEST" in category_name:
                    print("ezgfqk")
                    await ctx.channel.send(
                        "Ticket Approved!\nYour ticket has been approved and has been transferred through to the Management Team.\n1 point is added to your score"
                    )
                    #Once the proof is sent, we add 0.5p to the whitelist score
                    fol_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
                    author_index = fol_data[fol_data.mem_id == str(id_not_modBot)].index.tolist()[0]
                    c_times = fol_data.iloc[author_index, 3]
                    fol_data.iloc[author_index, 3] = c_times + 1
                    fol_data.to_csv(csv_file, index=False, sep='\t')
                 """

                if "SPAM" in category_name:
                    await ctx.channel.send(
                        "Ticket Approved!\n Thank you for reporting spam! 0.5 points will be added to your whitelist score."
                    )
                    """ Once the proof is sent, we add 0.5p to the whitelist score"""
                    fol_data = pd.read_csv(csv_file, sep="\t", dtype = {'mem_id': str})
                    author_index = fol_data[fol_data.mem_id == str(id_not_modBot)].index.tolist()[0]
                    e_times = fol_data.iloc[author_index, 12]
                    fol_data.iloc[author_index, 12] = e_times + 1
                    fol_data.to_csv(csv_file, index=False, sep='\t')
            else:
                await ctx.channel.send("Command <<v.approved>> already given.", delete_after=5.0)

client.run(bot_token)
