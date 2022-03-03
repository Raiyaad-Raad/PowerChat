#First we import some functions
import discord
from discord.ext import commands
import wikipedia,os
from chatbot import Chat, register_call

# You can put any prefix
prefix = "-"

bot = commands.Bot(command_prefix = prefix)
bot.remove_command(name="help")

#This code is for the AI
@register_call("whoIs") 
def who_is(query, session_id="general"):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

#This code is for the file of the AI, is very important
template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chatbotTemplate","chatbottemplate.template")

chat=Chat(template_file_path)

#This will say you in the shell when the bot is ready. This code is optional
@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()  
async def chat(ctx, *, message):
    result = chat.respond(message)
    if(len(result)<=2048):
        # embed=discord.Embed(title="ChatBot AI", description = result, color = (0xF48D1))
        await ctx.reply(content=result)
    else:
        embedList = []
        n=2048
        embedList = [result[i:i+n]for i in range(0, len(result), n)]
        for num, item in enumerate(embedList, start = 1):
            if(num == 1):
                embed = discord.Embed(title="PowerChat", description = item, color = (0xF48D1))
                embed.set_footer(text="Page{}".format(num))
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(description = item, color = (0xF48D1))
                embed.set_footer(text = "Page {}".format(num))
                await ctx.send(embed = embed)
@bot.command()  
async def ping(ctx):
  embed = discord.Embed(
    author = ctx.message.author,
    title = "Ping Checker",
    description = f"hello! before saying my ping you need to know ping so you can know how fast the bot response since it's in milesconds anyways here's the ping: {round(bot.latency * 1000)}ms",
    color = (0xF48D1)
  )

  await ctx.send(embed=embed)
  
@bot.command()  
async def help(ctx):
  embed = discord.Embed(
    author = ctx.message.author,
    title = "helper",
    description = f"hello! My commands in the field! BTW my prefix is **-** and wherever you see this bracket ***<*** this means you need to define it like -chat <message> and here you do is *-chat hi* the bot will response you like a human and you can continue the commmunication :)",
    color = (0xF48D1)
  )

  embed.add_field(name="ping", value="See my ping!", inline=True)
  embed.add_field(name="chat <message>", value="Oh Cmon Dude! Chat With Me!", inline=True)
  embed.set_footer(text=ctx.message.author)

  await ctx.send(embed=embed)


  





bot.run(os.environ['login'])