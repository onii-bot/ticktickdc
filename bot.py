import discord
from discord.ext import commands
from discord import app_commands, ui
from dotenv import load_dotenv
import os
from datetime import datetime
from main import add_task_to_ticktick

load_dotenv()

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

class MyModal(ui.Modal, title="Adding Task to TickTick"):
    def __init__(self):
        super().__init__(timeout=300)

        self.ttitle = ui.TextInput(label="Add title for the task: ", style=discord.TextStyle.short, placeholder="Title", required=True)
        self.description = ui.TextInput(label="Add description for the task: ", style=discord.TextStyle.long, placeholder="Description", default="", required=False)
        self.start_time = ui.TextInput(label="Add Start Time; Format(dddd-mm-dd-hh-mm)", style=discord.TextStyle.short, placeholder="Start Time", default=f"{datetime.now().strftime("%Y-%m-%d-%H-%M")}", required=True)
        self.end_time = ui.TextInput(label="Add End Time; Format(dddd-mm-dd-hh-mm)", style=discord.TextStyle.short, placeholder="End Time", default=f"{datetime.now().strftime("%Y-%m-%d-%H-%M")}", required=True)

    async def on_submit(self, interaction):
        add_task_to_ticktick(self.title, self.description, self.start_time, self.end_time)
        embed = discord.Embed(title=self.title, description=f"**{self.title}**\n{self.ttitle.label}:{self.ttitle}\n{self.description.label}:{self.description}:\n**Date:** {self.date.selected_date.strftime('%Y-%m-%d')}", timestamp=datetime.now(), color=discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


# @bot.tree.command(name="add_task")
# @app_commands.describe(task_name="task to add", task_description="descrition to add", start_time="date to add format(dddd-mm-dd-hh-mm)", end_time="date to end format(dddd-mm-dd-hh-mm)")
# async def add_task(interaction: discord.Interaction, task_name: str, task_description:str, start_time:str, end_time:str):
#     add_task_to_ticktick(task_name, task_description, start_time, end_time)
#     await interaction.response.send_message(f"{task_name} {task_description} {start_time} {end_time}")

@bot.tree.command(name="modal")
async def modall(interaction: discord.Interaction):
    await interaction.response.send_modal(MyModal())

bot.run(os.environ.get("DISCORD_TOKEN"))
