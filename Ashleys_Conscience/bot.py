import os
import hikari
import lightbulb
import requests
import json

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
@lightbulb.command("echo", "force words (or cock) into my mouth :3")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_echo(ctx: lightbulb.SlashContext) -> None:
    if "uwu_" == str(ctx.author).lower():
        await ctx.respond("Your thoughts are my thoughts, babe", flags=hikari.MessageFlag.EPHEMERAL)
        await bot.rest.create_message(ctx.channel_id, ctx.options.text)
    elif  ("cock" in ctx.options.text.lower()) or ("dick" in ctx.options.text.lower()) or "penis" in ctx.options.text.lower() or "anal" in ctx.options.text.lower() or "sex" in ctx.options.text.lower() or "gex" in ctx.options.text.lower():
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
    words = event.message.split()
    user = event.author

    with open("db.json", 'r') as file:
        db = json.load(file)
    file.close()

    for i in words:
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


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name="being cute :3", state="because Ashley is the cutest girl alive", type=hikari.ActivityType.COMPETING
        ))