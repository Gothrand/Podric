import discord, os
from discord import channel
from discord.ext import commands, tasks

class Pods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # This needs to be set to the #seed-mining-bot channel ID
        self.channel_id = 915030926474493993
        self.lastUpdate = None
        
    @commands.command(name='set', hidden=True, help="Set the channel ID the bot posts to.")
    async def set_channel(self, ctx, channel_id: int):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("`You do not have permission to use this command.`")
            return
        
        self.channel_id = channel_id
        await ctx.send("`Channel ID changed.`")

    # Defines the loop that will send messages on a given time interval.
    @tasks.loop(seconds=1)
    async def pod_msg(self):

        try:
            lastUpdate = os.path.getmtime(r"C:\Seeds\MapImage.png")
        except OSError as e:
            print(e)

        if lastUpdate != self.lastUpdate:
            self.lastUpdate = lastUpdate

            # needs channel ID
            message_channel = self.bot.get_channel(self.channel_id)
            
            with open(r"C:\Seeds\SeedsTest.txt", 'r') as f:
                seedData = f.readline()[:-1].split('!')[:-1]

            stage = seedData[0]
            seed = seedData[1]
            numPods = seedData[-1]
            tpPos = seedData[-2]
            pods = seedData[2:-2]
            file = discord.File("C:\Seeds\MapImage.png")
            await message_channel.send(embed=podEmbed(seed, numPods, stage), file=file)
        else:
            pass

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
    with open("resources/SeedsTest.txt", "r") as f:
        lines = f.readlines()
    
    for line in lines:
        yield line

def podEmbed(seed, numPods, stage):
    embedVar = discord.Embed(title=f"Seed: `{seed}`", color=0x6eb0e6)

    match stage:
        case "blackbeach":
            stage = "`Distant Roost 1`"
        case "blackbeach2":
            stage = "`Distant Roost 2`"
        case "golemplains":
            stage = "`Titanic Plains 1`"
        case "golemplains2":
            stage = "`Titanic Plains 2`"
        case _:
            stage = "`null`"
    embedVar.add_field(name="Pods", value=str(F"`{numPods}`"))
    embedVar.add_field(name="Stage", value=stage)
    embedVar.set_image(url="attachment://MapImage.png")
    # embedVar.set_image(url="https://drive.google.com/file/d/1-CWiM1p0TKNV0E_sogkTCmA7uU_Jg8pw/view")
    
    # embedVar.set_image(url="something")
    return embedVar