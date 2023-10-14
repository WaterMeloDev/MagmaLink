import discord
from discord.ext import commands
from discord import app_commands
import json
from colorama import Fore

class CONNECT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Fore.GREEN}[ OK ]{Fore.RESET} loaded connect.py")


    @app_commands.command(name="connect", description="connect to the guild link.")
    @app_commands.checks.has_permissions(administrator=True)
    async def connect_cmd(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.guild.owner.id:
            await interaction.response.send_message("Only the guild owner can connect the guild.")
            return

        # Get the guild ID and name
        guild_id = str(interaction.guild.id)
        guild_name = interaction.guild.name

        # Load the existing connected guilds from JSON file (if any)
        try:
            with open('src/data/guilds.json', 'r') as f:
                guilds = json.load(f)
        except FileNotFoundError:
            guilds = {}

        # Add the guild to the JSON data if not already connected
        if 'connected_guilds' not in guilds:
            guilds['connected_guilds'] = {}

        if guild_id not in guilds['connected_guilds']:
            guilds['connected_guilds'][guild_id] = guild_name
            with open('src/data/guilds.json', 'w') as f:
                json.dump(guilds, f, indent=4)

            embed = discord.Embed(title="Connected!", description=f"Successfully connected {guild_name} to link!", color=0x00ff00)
            embed.add_field(name="/disconnect", value="Disconnects guild from link.", inline=False)
            embed.add_field(name="/support", value="Shows ways to support the bot.", inline=False)
            embed.set_footer(text="You can now use the /help command in your server to see all the commands you can use with me!")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{guild_name} is already connected.")
    
    @app_commands.command(name="disconnect", description="disconnect from the guild link.")
    @app_commands.checks.has_permissions(administrator=True)
    async def disconnect_cmd(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.guild.owner.id:
            await interaction.response.send_message("Only the guild owner can disconnect the guild.")
            return

        # Get the guild ID and name
        guild_id = str(interaction.guild.id)
        guild_name = interaction.guild.name

        # Load the existing connected guilds from JSON file (if any)
        try:
            with open('src/data/guilds.json', 'r') as f:
                guilds = json.load(f)
        except FileNotFoundError:
            guilds = {}

        # Add the guild to the JSON data if not already connected
        if 'connected_guilds' not in guilds:
            guilds['connected_guilds'] = {}

        if guild_id in guilds['connected_guilds']:
            del guilds['connected_guilds'][guild_id]
            with open('src/data/guilds.json', 'w') as f:
                json.dump(guilds, f, indent=4)

            embed = discord.Embed(title="Disconnected!", description=f"Successfully disconnected {guild_name}!", color=0x00ff00)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{guild_name} is not connected.")

async def setup(bot):
    await bot.add_cog(CONNECT(bot))