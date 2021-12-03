import discord
from discord.ext import commands, tasks

class Pods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # This needs to be set to the #seed-mining-bot channel ID
        self.channel_id = 914637659320762399
        self.seeds = seedGen()

    # Defines the loop that will send messages on a given time interval.
    @tasks.loop(minutes=1)
    async def pod_msg(self):
        # needs channel ID
        message_channel = self.bot.get_channel(self.channel_id)
        seedData = next(self.seeds).split()

        stage = seedData[0]
        seed = seedData[1]
        numPods = seedData[2]
        tpPos = seedData[-1]

        # Pod coordinates will always start at index 2 and end before the last item in this schema
        pods = seedData[3:-1]

        await message_channel.send(embed=podEmbed(seed, numPods, stage))

    @commands.Cog.listener()
    async def on_ready(self):
        """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

        print(f'\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n')

        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("Pod Mining"))
        print(f'Successfully logged in!')

        self.pod_msg.start()

# Required to have the cog add successfully
def setup(bot):
    bot.add_cog(Pods(bot))

def seedGen():
    with open("resources/Seeds.txt", "r") as f:
        lines = f.readlines()
    
    for line in lines:
        yield line

def podEmbed(seed, numPods, stage):
    embedVar = discord.Embed(title=f"Seed: {seed}", color=0x6eb0e6)

    embedVar.add_field(name="Pods", value=str(numPods))
    embedVar.add_field(name="Stage", value=stage)
    
    # embedVar.set_image(url="something")
    return embedVar