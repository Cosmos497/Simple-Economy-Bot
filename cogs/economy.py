import discord
import aiosqlite
import random
from discord.ext.commands import cooldown, BucketType
from discord import Embed
from discord.ext import commands

# Remember that the code might not be the best. 

class currency(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.db = await aiosqlite.connect("myDB.db")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS userCurrency (user_id int, coins int, PRIMARY KEY (user_id))") # Creates a table inside of our Database called userCurrency

        print("Economy Cog Is Working")

    @commands.command()
    async def tester(self, ctx):
        await ctx.send("This is a test.")

    @commands.command()
    @cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        try:
            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (ctx.author.id, 1))
            amt = random.randint(5,15)
            print(amt)
            await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins + {amt} WHERE user_id = {ctx.author.id}")

            await self.bot.db.commit()
            await ctx.send(f"You earned {amt} coins!\nRun this command in 24 hours to claim more Coins!")
        except Exception as e:
            print(e)
            await ctx.send("There was an issue with this command.\nIf this continues, please join our help server!")

    @commands.command()
    async def bal(self, ctx, user : discord.Member = None):
        try:
            
            if user == None:
                user = ctx.author

            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (user.id, 1))

            async with self.bot.db.execute(f"SELECT coins FROM userCurrency WHERE user_id = {user.id}") as cursor:
                data = await cursor.fetchone()
                balance = data[0]
            
            if not balance == 1:
                await ctx.send(f"{user.name} has **{balance}** coins!")
            else:
                await ctx.send(f"{user.name} has **{balance}** coin!")
            await self.bot.db.commit()
        except Exception as e:
            print(e)
            await ctx.send("There was an issue with this command.\nIf this continues, please join our help server!")

    @commands.command(aliases=['gift', 'send'])
    async def send_money(self, ctx, user : discord.Member, amt = None):
        try:

            if user == ctx.author:
                await ctx.send("You cannot send money to your self.")
                return

            if amt == None:
                await ctx.send(f"You have to send at least ``1`` Coin to another user! {user.name}")
                
            amt = int(amt)

            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (ctx.author.id, 1))
            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (user.id, 1))


            async with self.bot.db.execute(f"SELECT coins FROM userCurrency WHERE user_id = {ctx.author.id}") as cursor:
                data = await cursor.fetchone()
                balance = data[0]
            
            if balance < amt:
                await ctx.send("You don't have enough Coins!")
                

            elif amt < 1:
                await ctx.send("You need to send at least ``1`` Coin!")
            
            
            if balance > 0:
                await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins - {amt} WHERE user_id = {ctx.author.id}")
                await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins + {amt} WHERE user_id = {user.id}")
                
                await ctx.send(f"{ctx.author.mention} has sent {amt} coins to {user.mention}")

            await self.bot.db.commit()

        except Exception as e:
            await ctx.send(f"There was an issue when you were sending money to {user.name}")
        


    @commands.command(aliases=['slot'])
    async def slots(self, ctx, wager : int):
        try:
            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (ctx.author.id, 1))
            async with self.bot.db.execute(f"SELECT coins FROM userCurrency WHERE user_id = {ctx.author.id}") as cursor:
                data = await cursor.fetchone()
                balance = data[0]

            if balance >= wager:
                if balance > 15:
                    final = []
                    slotstr = "╢"
                    for x in range(3):
                        a = random.choice([":seven:",":o2:",":regional_indicator_q:"])
                        final.append(a)
                        slotstr = slotstr+a
                    slotstr = slotstr+f"╟ 📍\n\n**Bet: `${wager}`**"

                    embed = discord.Embed(
                        colour=0xfcb103,
                        title="Slot Machine",
                        description=slotstr
                    )
                    await ctx.send(embed=embed)
                    if final[0] == final [1] == final [2]:
                        wager = wager*3
                        await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins + {wager} WHERE user_id = {ctx.author.id}")
                        await ctx.send(f"You won the Jack Pot!\nYour prize is **{wager}**")
                    else:
                        wager = wager*2
                        balance2 = balance - wager
                        if balance2 <= 0:
                            await self.bot.db.execute(f"UPDATE userCurrency SET coins = 0 WHERE user_id = {ctx.author.id}")
                            await ctx.send(f"You lost all your money :(")
                        else:
                            await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins - {wager} WHERE user_id = {ctx.author.id}")
                            await ctx.send(f"You lost {wager}")
                else:
                    await ctx.send("You need to wager at least ``15`` Coins!")

            else:
                await ctx.send("You don't have enough Coins.")

            await self.bot.db.commit()

        except Exception as e:
            print(e)
            await ctx.send("There was an issue with this command.\nIf this continues, please join our help server!")

    @commands.command(aliases=['wager','flip','flipcoin'])
    async def coinflip(self, ctx, headortails : str, wager : int):
        try:
            await self.bot.db.execute("INSERT OR IGNORE INTO userCurrency (user_id, coins) VALUES (?,?)", (ctx.author.id, 1))
            async with self.bot.db.execute(f"SELECT coins FROM userCurrency WHERE user_id = {ctx.author.id}") as cursor:
                data = await cursor.fetchone()
                balance = data[0]

            if balance >= wager:
                if balance > 15:
                    chance = random.randrange(2)
                    if chance == 1 and headortails == "heads":
                        wager += wager 
                        await ctx.send(f"You got Heads!\nYou won **{wager}** Coins!")
                        await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins + {wager} WHERE user_id = {ctx.author.id}")

                    elif chance == 0 and headortails == "tails":
                        await ctx.send(f"You got Tails!\nYou won **{wager}** Coins!")
                        await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins + {wager} WHERE user_id = {ctx.author.id}")

                    elif chance == 0 and headortails == "heads" or chance == 1 and headortails == "tails":
                        wager += wager
                        neobalance = balance - wager
                        await ctx.send(f"You got Tails!!\nYou lost **{wager}**")
                        if neobalance <= 0:
                            await self.bot.db.execute(f"UPDATE userCurrency SET coins = 0 WHERE user_id = {ctx.author.id}")
                        else:
                            await self.bot.db.execute(f"UPDATE userCurrency SET coins = coins - {wager} WHERE user_id = {ctx.author.id}")

                    else:
                        await ctx.send("wYou can only wager ``heads`` or ``tails``!")

                else:
                    await ctx.send("You need to wager at least ``15`` Coins!")
            else:
                await ctx.send("You don't have enough Coins.")

            await self.bot.db.commit()

        except Exception as e:
            print(e)
            await ctx.send("There was an issue with this command.\nIf this continues, please join our help server!")

        

def setup(bot):
    bot.add_cog(currency(bot))