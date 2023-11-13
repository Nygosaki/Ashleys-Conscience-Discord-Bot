import os
import hikari
import lightbulb
import requests
import json
import dotenv

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    token=os.environ["TOKEN"],
    default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True,
    intents=hikari.Intents.ALL,
)


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    print(event)


@bot.command()
@lightbulb.option("text", "The thing in my mouth :3", required=True)
@lightbulb.command("echo", "force words into my mouth :3")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_echo(ctx: lightbulb.SlashContext) -> None:
    if "uwu_" == str(ctx.author).lower():
        await ctx.respond("Your thoughts are my thoughts, babe", flags=hikari.MessageFlag.EPHEMERAL)
        await bot.rest.create_message(ctx.channel_id, ctx.options.text)
    elif  ("cock" in ctx.options.text.lower()) or ("dick" in ctx.options.text.lower()) or "penis" in ctx.options.text.lower() or "anal" in ctx.options.text.lower() or "sex" in ctx.options.text.lower() or "gex" in ctx.options.text.lower() or "cheating" in ctx.options.text.lower():
        await ctx.respond(f"Did you just try to make me cheat on my gf >:(")
    else:
        if "love" in ctx.options.text.lower():
            await ctx.respond("Awwww, love you tooo :>", flags=hikari.MessageFlag.EPHEMERAL)
        elif "sloppy toppy" in ctx.options.text.lower():
            await ctx.respond("The immigrants are taking our jobs >:(", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            await ctx.respond("If you are  making me say mean things I will commit arson", flags=hikari.MessageFlag.EPHEMERAL)
        await bot.rest.create_message(ctx.channel_id, ctx.options.text)


@bot.command()
@lightbulb.option("choice", "The kind of quote you want me to get", required=False, default="", choices=['alone', 'anger', 'attitude', 'beauty', 'business', 'computers', 'dating', 'death', 'dreams', 'fear', 'forgiveness', 'friendship', 'funny', 'good', 'happiness', 'home', 'hope', 'humor', 'failure' , 'intelligence', 'jealousy', 'knowledge', 'life', 'love', 'marriage'])
@lightbulb.command("quote", "Figure out some kind of quote")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_quote(ctx: lightbulb.SlashContext) -> None:
    r = requests.get(url=f"https://api.api-ninjas.com/v1/quotes?category={ctx.options.choice}", headers={"X-Api-Key": os.environ["QOUTE_API"]})
    await ctx.respond(r.json()[0]["quote"])


@bot.command()
@lightbulb.command("inspiration", "You want inspiration? Are you sure you will want it in 10s?")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_inspiration(ctx: lightbulb.SlashContext) -> None:
    url = "https://inspirobot.me/api?generate=true"
    # Fetch the HTML of the website
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        await ctx.respond(html)
    else:
        await ctx.respond("Failed to fetch HTML. Status code: {response.status_code}", flags=hikari.MessageFlag.EPHEMERAL)

@bot.listen()
async def messageLog(event: hikari.GuildMessageCreateEvent) -> None:
    sentence = event.message.content
    
    words = str(event.message.content).split()
    user = str(event.message.author).lower()
    if user == "ashely's conscience#6213" and "word" in str(event.message.content).lower():
        return

    with open("db.json", 'r') as file:
        db = json.load(file)
    file.close()

    for i in words:
        i = i.lower()
        if len(i) > 11:
            break
        try:
            if db[user]:
                try:
                    db[user][i] += 1
                except KeyError:
                    db[user][i] = 1
        except KeyError:
                db[user] = {i: 1}

    with open("db.json", 'w') as file:
        json.dump(db, file)
    file.close()
    if "femboy" in sentence or "furry" in sentence:
        await bot.rest.create_message(event.get_channel(), "O")
    elif "cute" in sentence:
        await bot.rest.create_message(event.get_channel(), "And who might that be? :3")
    elif "milo" in sentence:
        await bot.rest.create_message(event.get_channel(), "WOOF WOOF")
    elif "<3" in sentence:
        await bot.rest.create_message(event.get_channel(), "I love you too Milo :>")
    elif "antichrist" in sentence:
        await bot.rest.create_message(event.get_channel(), "I know someoe superior :3")
    

@bot.command()
@lightbulb.option("user", "Who do you want me to snitch on? :3", required=True)
@lightbulb.command("word-count", "See who said what :3")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_word_count(ctx: lightbulb.SlashContext) -> None:
    try:
        with open("db.json", 'r') as file:
            db = json.load(file)
        userWords = sorted(db[str(ctx.options.user).lower()].items(), key=lambda x:x[1], reverse=True)
        file.close()
        def encodeWords(userWords):
            out = "```\n+------------+--------+\n| Word       | Amount |\n+------------+--------+\n"
            flag = 0
            for i in userWords:
                flag += 1
                out += f"| {str(i[0]).ljust(11)}| {str(i[1]).ljust(7)}|\n"
                if flag == 10:
                    break
            out += f"+------------+--------+```"
            return out
        embed = hikari.Embed(title=f"What has come out of {ctx.options.user}'s mouth?", description=encodeWords(userWords))
        embed.set_footer("Please know that only messages sent while the bot is online are considered")
        await ctx.respond(embed=embed)
    except:
        await ctx.respond(f"{str(ctx.options.user)} is not a tracked user, or has not said enough words", flags=hikari.MessageFlag.EPHEMERAL)
    


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name="being cute :3", state="because Ashley is the cutest girl alive", type=hikari.ActivityType.COMPETING
        ))
    
run()