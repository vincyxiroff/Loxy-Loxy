import discord
from requests import get
from discord.ext import commands
from datetime import datetime
from time import time as __, sleep as zzz
from re import findall

ec= 0xFF0036

token=""
status="asnathedev on top"

def log(text,sleep=None): 
    print(f"[{datetime.utcfromtimestamp(__()).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")
    if sleep: zzz(sleep)

bot = commands.Bot(command_prefix='dc!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    log(f"Connected to {bot.user}",0.5)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Activity(name=status, type=2))


@bot.hybrid_command(name="vc", description="Check if the cookie is valid", with_app_command=True)
async def vc(ctx, cookie=None):
    await ctx.defer()
    if not cookie:
        em1 =discord.Embed(color=ec)
        em1.add_field(name=":x: Missing Cookie", value="TheBestChecker")
        await ctx.send(embed=em1,ephemeral=True)
        log(f'User {ctx.author} tried to use /vc but did not provide a cookie.')
        return
    #await ctx.message.delete()
    response = get('https://users.roblox.com/v1/users/authenticated',cookies={'.ROBLOSECURITY': cookie})
    if '"id":' in response.text:
        log(f'User {ctx.author} used /vc with a valid cookie.')
        em2 = discord.Embed(color=0x38d13b)
        em2.add_field(name=":white_check_mark: Valid Cookie", value="check dms")
        
        dm = await ctx.author.create_dm()
        await dm.send("------ Cookie Check ------" + "\n" + "```" + cookie + "```" + "\n" + "------ End Cookie Check ------")
        await ctx.send(embed=em2)
    elif 'Unauthorized' in response.text:
        log(f'User {ctx.author} used /vc with an invalid cookie.')
        await ctx.send("invalid or not working cookie", ephemeral=True)
    else:
        log(f'User {ctx.author} used /vc but roblox returned a bad response.')
        em4=discord.Embed(color=0xFFFF00)
        em4.add_field(name=":x: Error", value='```'+response.text+'```', inline=False)
        await ctx.send(embed=em4,ephemeral=True)

@bot.hybrid_command(name='vcr', description="check if cookie is valid + show robux balance", with_app_command=True)
async def vcr(ctx, cookie=None):
    await ctx.defer()
    if not cookie:
        em5=discord.Embed(color=0xFF0000)
        em5.add_field(name=":x: Missing Cookie",value="")
        await ctx.send(embed=em5,ephemeral=True)
        log(f'User {ctx.author} tried to use /vcr but did not provide a cookie.')
        return
  #  await ctx.message.delete()
    response = get('https://users.roblox.com/v1/users/authenticated',cookies={'.ROBLOSECURITY': cookie})
    if '"id":' in response.text:
        log(f'User {ctx.author} used /vcr with a valid cookie.')
        user_id = response.json()['id']
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency',cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        em6=discord.Embed(color=0x38d13b)
        em6.add_field(name=":white_check_mark: Valid Cookie", value="")
        em6.add_field(name="Passed Cookie: ", value='```Hidden```', inline=False)
        em6.add_field(name=":money_mouth: Robux", value=robux, inline=True)
        dm = await ctx.author.create_dm()
        await dm.send("cookie: " + "\n" + '```' + cookie + '```' + "Robux: " + "\n")
        await dm.send("------ VCR ------" + "\n" + '```' + str(robux) + '```' + "\n" + "------ END VCR ------")
        await ctx.send(embed=em6)
    elif 'Unauthorized' in response.text:
        log(f'User {ctx.author} used /vcr with an invalid cookie.')
        await ctx.send("invalid or not working cookie", ephemeral=True)
    else:
        log(f'User {ctx.author} used /vcr but roblox returned a bad response.')
        em8=discord.Embed(color=0xFFFF00)
        em8.add_field(name=":x: Error", value='```'+response.text+'```', inline=False)
        await ctx.send(embed=em8,ephemeral=True)


@bot.hybrid_command(name='full', description="display everything about the account", with_app_command=True)
async def full(ctx,cookie=None):
    await ctx.defer()
    if not cookie:
        emb1=discord.Embed(color=0xFF0000)
        emb1.add_field(name=":x: Missing Cookie",value="")
        await ctx.send(embed=emb1,ephemeral=True)
  #  await ctx.message.delete()
    response = get('https://users.roblox.com/v1/users/authenticated',cookies={'.ROBLOSECURITY': cookie})
    hidden = '```Hidden```'
    if '"id":' in response.text:
        user_id = response.json()['id']
        # ----- 
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency',cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        # ----- 
        balance_creit_info = get(f'https://billing.roblox.com/v1/credit',cookies={'.ROBLOSECURITY': cookie})
        # ----- 
        balance_credit = balance_creit_info.json()['balance']
        balance_credit_currency = balance_creit_info.json()['currencyCode']
        # ----- 
        account_settings = get(f'https://www.roblox.com/my/settings/json',cookies={'.ROBLOSECURITY': cookie})
        # -----
        account_name = account_settings.json()['Name']
        account_display_name = account_settings.json()['DisplayName']
        account_email_verified = account_settings.json()['IsEmailVerified']
        if bool(account_email_verified):
            account_email_verified = f'{account_email_verified} (`{account_settings.json()["UserEmail"]}`)'
        account_above_13 = account_settings.json()['UserAbove13']
        account_age_in_years = round(float(account_settings.json()['AccountAgeInDays']/365),2)
        account_has_premium = account_settings.json()['IsPremium']
        account_has_pin = account_settings.json()['IsAccountPinEnabled']
        account_2step = account_settings.json()['MyAccountSecurityModel']['IsTwoStepEnabled']
        # -----
        emb55 = discord.Embed(color=0x38d13b)
        emb55.add_field(name=":white_check_mark: Valid Cookie", value="deam")
        emb55.add_field(name=":money_mouth: Robux", value=str(robux) + "\n" + "Has PIN: " + str(account_has_pin) + "\n" + "check dm for other", inline=True) 
        account_friends = get('https://friends.roblox.com/v1/my/friends/count',cookies={'.ROBLOSECURITY': cookie}).json()['count']
        account_voice_verified = get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}).json()['isVerifiedForVoice']
        account_gamepasses = get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={user_id}',cookies={'.ROBLOSECURITY': cookie})
        check = findall(r'"PriceInRobux":(.*?),', account_gamepasses.text)
        account_gamepasses = str(sum([int(match) if match != "null" else 0 for match in check]))+f' R$'
        account_badges = ', '.join(list(findall(r'"name":"(.*?)"',get(f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges',cookies={'.ROBLOSECURITY': cookie}).text)))
        account_transactions = get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary',cookies={'.ROBLOSECURITY': cookie}).json()
        account_sales_of_goods = account_transactions['salesTotal']
        account_purchases_total = abs(int(account_transactions['purchasesTotal']))
        account_commissions = account_transactions['affiliateSalesTotal']
        account_robux_purchcased = account_transactions['currencyPurchasesTotal']
        account_premium_payouts_total = account_transactions['premiumPayoutsTotal']
        account_pending_robux = account_transactions['pendingRobuxTotal']
        dm = await ctx.author.create_dm()
        await ctx.send(embed=emb55)
        await dm.send("```------ Full ------ ```" + "\n" + "Cookie: " + "\n" + "```" + cookie + "```" + "\n" + "Robux: " + str(robux) + "\n" + "Account Name & Display name" + "\n" + account_name + " " + account_display_name + "\n" + "Age in years: " + str(account_age_in_years) + "\n" + "Game pass Worth: " + str(account_gamepasses) + "\n" + "Sales Of Goods" + str(account_sales_of_goods) + "\n" + "Pending Robux" + str(account_pending_robux) + "\n" + "VoiceChat Verified: " + str(account_voice_verified) + "\n" + "Has pin: " + str(account_has_pin) + "\n" + "email: " + account_email_verified + "\n" + "------ End Full ------")
        
    elif 'Unauthorized' in response.text:
        log(f'User {ctx.author} used /full with an invalid cookie.')
        await ctx.send("invalid or not working cookie", ephemeral=True)
    else:
        log(f'User {ctx.author} used /full but roblox returned a bad response.')
        emb3=discord.Embed(color=0xFFFF00)
        emb3.add_field(name=":x: Error", value='```'+response.text+'```', inline=False)
        await ctx.send(embed=emb3,ephemeral=True)


bot.run(token)
