import discord, os
from discord.ext import commands, tasks

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initialize the bot
bot = commands.Bot(command_prefix='!', description='Posting Pod Seeds Twice Daily')

# List of cogs that we can optionally add, not really needed for podric right now
initial_extensions = ['cogs.admin',
                      'cogs.pods']

def main():
    for extension in initial_extensions:
        bot.load_extension(extension)

if __name__ == "__main__":
    main()
    bot.run(TOKEN)
