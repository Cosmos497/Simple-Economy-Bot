import discord
from discord.ext import commands
import json

bot = commands.Bot("..")

@bot.event
async def on_ready():
    print(f"Economy bot ready")


@bot.command()
async def test(ctx):
    await ctx.send("Testing!")


if __name__ == "__main__":
    extensions = ["cogs.economy"] #loads your cogs
    if __name__ == '__main__':
        for extension in extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(e)
    # Make a json file in the root dir called "bot_config.json" with a single field called "bot_token"
    with open(file="bot_config.json") as f:
        token = json.load(f)["bot_token"]
    bot.run(token)
