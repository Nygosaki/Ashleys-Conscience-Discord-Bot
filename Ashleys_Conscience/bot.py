import os
import hikari
import lightbulb
import requests
import json
import dotenv
import smtplib, ssl
import re
import dns.resolver
import miru
import time
from email.message import EmailMessage

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    token=os.environ["TOKEN"],
    help_slash_command=True,
    intents=hikari.Intents.ALL,
)

miru.install(bot)

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    print(event)


class MyView(miru.View):
    def __init__(self, timeout, sender, reciever, em):
        self.sender = sender
        self.reciever = reciever
        self.em = em
        super().__init__(timeout=timeout)

    @miru.button(label="Yes", emoji="\N{White Heavy Check Mark}", style=hikari.ButtonStyle.SUCCESS)
    async def yes_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # await ctx.respond("Paper!")
        try:
            smtpSever = os.getenv("SMTPSERVER")
            smtpSeverPort = os.getenv("SMTPSERVERPORT")
            smtpServerUser = os.getenv("SMTPSERVERUSER")
            smtpServerToken = os.getenv("SMTPSERVERTOKEN")
        except:
            await ctx.respond(".env information was unable to be loaded properly")
            return True
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtpSever, smtpSeverPort) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(smtpServerUser, smtpServerToken)
                server.send_message(self.em, from_addr=self.sender, to_addrs=self.reciever)
        except Exception as exception:
            await ctx.respond("Error: %s!\n\n" % exception)
        await ctx.respond('Email sent!')
        self.stop()

    @miru.button(label="No", emoji="\N{Cross Mark}", style=hikari.ButtonStyle.DANGER)
    async def no_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # await ctx.respond("Scissors!")
        await ctx.respond("You hanve canceled the action")
        self.stop()

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
    if user == "ashely's conscience#6213" and "word" in str(event.message.content).lower(): return

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
    if sentence == None: return
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
@lightbulb.option("senderemail", "The sender email address", required=True)
@lightbulb.option("sendername", "The sender name/nickname", required=True)
@lightbulb.option("recipient", "The recipient's email address", required=True)
@lightbulb.option("subject", "The subject of the email", required=True)
@lightbulb.option("body", "The text in the body of the email", required=True)
@lightbulb.option("replyto", "The email adress replyes should be sent to", required=True)
@lightbulb.command("emailsmtp", "Send SMTP emails through me", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def email_smtp(ctx: lightbulb.SlashContext) -> None:
    flag = False
    for x in ctx.member.role_ids:
        if x == 1047622446129365043:
            flag = True
            await ctx.respond("My SMTP will do whatever mommy requires :3")
    if flag == False:
        await ctx.respond("Who thoust dare touch my SMTP")
        return True
    
    sender = ctx.options.senderemail
    senderName = ctx.options.sendername
    reciever = ctx.options.recipient
    subject = ctx.options.subject
    content = ctx.options.body
    replyto = ctx.options.replyto

    em = EmailMessage()
    em['From'] = f"{senderName} <{sender}>"
    em['To'] = reciever
    em['Subject'] = subject
    em['Reply-To'] = replyto
    em.set_content(content)


    domain = re.split("@", sender)[1]
    await ctx.respond("Testing domain " + domain + " for DMARC record...")
    try:
        test_dmarc = dns.resolver.resolve('_dmarc.' + domain, 'TXT')
        for dns_data in test_dmarc:
            if 'DMARC1' in str(dns_data):
                await ctx.respond ("DMARC record found :" + str(dns_data))
                dmarc_sort = dict()
                try:
                    dmarc_sort["p"] = re.findall('p=(.*?)[; \n]', str(dns_data))[0]
                    if dmarc_sort["p"].lower() == "quarantine":
                        await ctx.respond("Warning: Your email will go to spam or be filtered")
                except:
                    dmarc_sort["p"] = "null"
                    await ctx.respond("There seems to be something wrong with the `p` value")
                try:
                    dmarc_sort["sp"] = re.findall('sp=(.*?)[; \n]', str(dns_data))[0]
                    if dmarc_sort["sp"] != dmarc_sort["p"]:
                        await ctx.respond(f"the `sp` record is not the same as `p`. `sp: {dmarc_sort['sp']}")
                except:
                    dmarc_sort["sp"] = dmarc_sort["p"]
                try:
                    dmarc_sort["pct"] = re.findall('pct=(.*?)[; \n]', str(dns_data))[0]
                    if dmarc_sort["p"].lower() == "reject" and str(dmarc_sort["pct"]) == "100":
                        await ctx.respond("The email will be rejected")
                        return True
                    else:
                        await ctx.respond(f"There is a {dmarc_sort['pct']}% chance that the `p` policy will be enforced")
                except:
                    dmarc_sort["pct"] = "100"
                    if dmarc_sort["p"].lower() == "reject":
                        await ctx.respond("The email will be rejected")
                        return True
                try:
                    dmarc_sort["fo"] = re.findall('fo=(.*?)[; \n]', str(dns_data))[0]
                    if "0" in dmarc_sort["fo"]:
                        await ctx.respond("fo=0: Generate a DMARC failure report if all underlying authentication mechanisms (SPF and DKIM) fail to produce an aligned “pass” result.")
                    if "1" in dmarc_sort["fo"]:
                        await ctx.respond("fo=1: Generate a DMARC failure report if any underlying authentication mechanism (SPF or DKIM) produced something other than an aligned “pass” result.")
                    if "d" in dmarc_sort["fo"]:
                        await ctx.respond("fo=d: Generate a DKIM failure report if the message had a signature that failed evaluation, regardless of its alignmen")
                    if "s" in dmarc_sort["fo"]:
                        await ctx.respond("fo=s: Generate an SPF failure report if the message failed SPF evaluation, regardless of its alignment.")
                except:
                    dmarc_sort["fo"] = "0"
                    await ctx.respond("fo=0: Generate a DMARC failure report if all underlying authentication mechanisms (SPF and DKIM) fail to produce an aligned “pass” result. (Default)")
                try:
                    dmarc_sort["ruf"] = re.findall('ruf=(.*?)[; \n]', str(dns_data))[0]
                    await ctx.respond(f"ruf: {dmarc_sort['ruf']}")
                except:
                    dmarc_sort["ruf"] = "none"
                try:
                    dmarc_sort["rua"] = re.findall('rua=(.*?)[; \n]', str(dns_data))[0]
                    await ctx.respond(f"rua: {dmarc_sort['rua']}")
                except:
                    dmarc_sort["rua"] = "none"

                await ctx.respond(dmarc_sort)
    except:
        await ctx.respond ("DMARC record not found.")
        pass
    view = MyView(timeout=60, sender=sender, reciever=reciever, em=em)  # Create a new view
    message = await ctx.respond("Considering this information, would you still like to continue?", components=view)
    await view.start(message)  # Start listening for interactions
    await view.wait() # Optionally, wait until the view times out or gets stopped


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

@bot.command()
@lightbulb.command("test", "test desc", guilds=(1040093928097054781))
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_test(ctx: lightbulb.SlashContext) -> None:
    ctx.respond("Watcha doin here? :3")


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name="being cute :3", state="because Ashley is the cutest girl alive", type=hikari.ActivityType.COMPETING
        ))
    
run()