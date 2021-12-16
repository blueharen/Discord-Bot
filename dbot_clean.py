# shoutout @greg

import discord
import pandas as pd
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib.request
import random
import requests

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game('worlds BEST bot'))

def get_soup(link):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(link, headers=hdr)
    page = req.content
    return(BeautifulSoup(page, 'html.parser'))

def get_stats(html_page, player_names, name_of_text, stat_name, indices_to_add=11, index_number=1):
    stat_list = []
    for p in html_page.find_all('table', {'class', 'stats table is-fullwidth table is-hoverable'}):
        if p.find_all('th')[index_number].text == name_of_text:
            for x in p.findChildren('td'):
                stat_list.append(x.text)

    stat_list = [item.strip() for item in stat_list]

    i = 0
    indices = []
    for x in stat_list:
        if x in player_names:
            indices.append(i)
        i = i + 1

    return_list = []
    for j in indices:
        return_list.append(f'{stat_list[j]} {stat_name}: {stat_list[j+indices_to_add]}')

    return(return_list)

@client.command()
async def speed(ctx, stat_name='speed', user='alex', player1='Spurx', player2='greg', player3='Alex'):
    #parameters:
    #   stat_name: speed = speed, ps = powerslide, off = offensive 1/3, bws = Boost While Supersonic
    #                        bpc = big pads collected, air = high air time, bpm = boost per minute,
    #                        0boost = time with 0 boost,
    #                        all = all stats
    #       NOTE: Allows for multiple stats: ps+air will give powerslide and air time stats only
    #
    #   user: person's profile to go off of.
    #   player[1-3]: names of players you wish to see

    all_stats = ['bws', 'bpm', 'bpc', '0boost', 'off', 'air', 'speed', 'ps']

    if stat_name == 'help':
        await ctx.send('Example of command specifying stat, profile, and players: \n!speed ps alex Player1 Squishy Musty')
        await ctx.send('All stats: \nspeed: Time supersonic. \nps: Number of powerslides. \noff: Time in offensive 1/3d. \nbws: Boost used while supersonic. \nbpc: Big boost pads collected. \nair: High air time. \nbpm: Boost Per Minute. \n0boost: Time with 0 boost. \nall: All stats listed. \nps+bws List multiple stats.')
        return(0)

    # Can't do this anymore since it allows for stat1+stat2
    # if stat_name not in all_stats:
    #     await ctx.send("Please enter a valid stat you'd like to see. stat_name !speed help for more options.")
    #     return(0)

    user = user.lower()
    if user == 'spurx':
        link = 'https://ballchasing.com/?player-name=Steam%3a76561198086495624'
    elif user == 'greg':
        link = 'https://ballchasing.com/?player-name=Steam%3a76561198110848400'
    elif user == 'alex':
        link = 'https://ballchasing.com/?player-name=Steam%3a76561198408828200'
    else:
        await ctx.send("Invalid User. Current Profile options: alex, spurx, greg")
        return(0)

    soup = get_soup(link)

    #names = ['Spurx','greg','Alex']
    names = [player1, player2, player3]

    #grab most recent replay from webpage
    try:
        link = 'https://ballchasing.com' + soup.select('.creplays li a')[1]['href']
    except IndexError as e:
        await ctx.send("ERROR: ballchasing.com is currently down.")
        return(0)

    #now scrape the new webpage
    soup = get_soup(link)

    stat_table_names =  ['BPM', 'BPM', 'BPM', 'BPM', 'Off. 1/3', 'Avg.Speed %', 'Avg.Speed %', 'Avg.Speed %']
    stat_print_names =  ['Boost While Supersonic', 'BPM', 'Big Pads Collected', 'Time with 0 Boost', 'Off. 1/3', 'High Air Time', 'Time Supersonic', 'Powerslides']
    indices_add_list =  [11, 1, 7, 3, 3, 9, 6, 11]
    index_number_list = [1, 1, 1, 1, 3, 2, 2, 2]

    ################################################################
    #E.G. speed+ps WILL RETURN STATS FOR SPEED AND PS ONLY
    ################################################################

    stat_names = stat_name.split("+")
    if stat_name == 'all':
        stat_names = all_stats

    stat_indices = [i for i in range(len(all_stats)) if all_stats[i] in stat_names]

    for j in stat_indices:
        for value in get_stats(soup, names, stat_table_names[j], stat_print_names[j], indices_to_add=indices_add_list[j], index_number=index_number_list[j]):
            await ctx.send(value)

@client.command()
async def reaction(ctx):
    reaction_list = [
                    '<:dbot:920734310259118081>',
                    '<:thatsg:912905125784334336>',
                    '<:99:912912697589375026>',
                    '<:gang:912911681590558752>',
                    '<:shnick:912903654212775976>',
                    '<:online:907126393077366784>',
                    '<:xd:847275152071983104>',
                    '<:patcar:846937361120231524>',
                    '<:knee:819453990026215424>',
                    '<:hand:819453734484049960>',
                    '<:programminggod:818871904827473970>',
                    '<:king:818871886594703431>',
                    '<:flightgod:818871857293951057>']

    reaction = random.choice(reaction_list)
    await ctx.send(reaction)

@client.command()
async def pleb(ctx):
    await ctx.send('pleb')

@client.command()
async def roast(ctx, name='None'):
    if name == 'None':
        name = str(ctx.author)

    replies = []

    roast = random.choice(replies)
    roast = roast.replace('name', name)
    await ctx.send(roast)

@client.command()
async def commend(ctx, name='None'):
    if name == 'None':
        name = str(ctx.author)

    replies = []

    toast = random.choice(replies)
    toast = toast.replace('name', name)
    await ctx.send(toast)

@client.command()
async def pog(ctx):
    replies = []

    await ctx.send(random.choice(replies))

@client.command()
async def quote(ctx):
    quotes = []

    quote = random.choice(quotes)
    await ctx.send(quote)

@client.command()
async def rps(ctx, choice='none'):
    if choice == 'none':
        await ctx.send('Try !rps rock')
    elif choice == 'rock':
        await ctx.send('Paper, you lose')
    elif choice == 'paper':
        await ctx.send('Scissors, you lose')
    elif choice == 'scissors':
        await ctx.send('Rock, you lose')

@client.command()
async def gamblehelp(ctx):
    embed = discord.Embed(title='!gamble help')
    embed.add_field(name='!gamble {amount}', value='Classic Wager. Gamble x amount of money for 1.15:1 return. 40% payout chance.')
    embed.add_field(name='!gamble {amount} {value}', value='Roulette. Values: red, black, zero. Red/black: 1:1 return, 48% payout chance. Zero: 24:1 return, 7% payout chance.')
    await ctx.send(embed=embed)

@client.command()
async def leaderboard(ctx):
    gambling_df = pd.read_csv('gambling.csv')
    gambling_df = gambling_df.sort_values('Amount', ascending=False)
    gambling_df = gambling_df.reset_index().drop('index', axis=1)

    embed = discord.Embed(title='Richest boys')

    for x in range(len(gambling_df)):
        embed.add_field(name=gambling_df.Name[x], value=str(float(gambling_df.Amount[x])), inline=True)

    await ctx.send(embed=embed)

@client.command()
async def freebie(ctx):
    FREEBIE_AMOUNT = 100

    gambling_df = pd.read_csv('gambling.csv')
    user = str(ctx.author)
    current_funds = int(gambling_df.loc[gambling_df.Name == user, 'Amount'])

    if current_funds < 0:
        await ctx.send("wow you're in the negative you really screwed up, sorry")
    elif current_funds == 0:
        gambling_df.loc[gambling_df.Name == user, 'Amount'] += FREEBIE_AMOUNT
        await ctx.send(f"Here's ${FREEBIE_AMOUNT}. Don't lose it!")
        gambling_df.to_csv('gambling.csv', index=False)
    else:
        await ctx.send("You're not broke yet")

@client.command()
@commands.check_any(commands.is_owner())
async def give(ctx, user, amount):
    gambling_df = pd.read_csv('gambling.csv')
    gambling_df.loc[gambling_df.Name == user, 'Amount'] += int(amount)
    await ctx.send(f"Added {amount} to {user}'s account.")
    gambling_df.to_csv('gambling.csv', index=False)

@client.command()
async def gamble(ctx, amount=0, color='None'):
    user = str(ctx.author)
    gambling_df = pd.read_csv('gambling.csv')
    current_funds = int(gambling_df.loc[gambling_df.Name == user, 'Amount'])

    outcome = 'Win!'
    li = [1,2,3,4,5,6,7,8,9,10]
    randint = random.randrange(1,104)

    if current_funds < 0:                                                       #BRANCH FOR negative funds
        await ctx.send('Beg Brad to give you more funds')

    elif amount > current_funds:
        await ctx.send('Too high of a bet')

    elif amount <= 0:                                                           #BRANCH FOR !gamble -{amount}
        await ctx.send('Try !gamble {amount} or !gamble {amount} red')

    elif (color != 'None') and color not in ['red','black','zero']:
        await ctx.send("Invalid input. Choose: 'red', 'black', 'zero'")

    elif (color != 'None') and (color in ['red','black','zero']):               #BRANCH FOR !gamble {amount} {color}

        if randint <= 48: roll = 'red'
        elif randint <= 96: roll = 'black'
        else: roll = 'zero'

        if (color == roll) and (color != 'zero'): amount = amount #1:1 reward
        elif color == roll: amount += amount*24 #24:1 reward
        else:
            amount = -amount #1:1 loss
            outcome = 'Loss!' #for display

        gambling_df.loc[gambling_df.Name == user, 'Amount'] += amount #updates database of total amount
        await ctx.send(f'{outcome} New total: {int(gambling_df.loc[gambling_df.Name == user, "Amount"])}') #displays total amount
        gambling_df.to_csv('gambling.csv', index=False)

    else:                                                                       #BRANCH FOR !gamble {amount}
        if random.choice(li) <= 4: #40% chance
            amount += amount*1.15
        else:
            amount = -amount
            outcome = 'Loss!'

        gambling_df.loc[gambling_df.Name == user, "Amount"] += amount
        await ctx.send(f'{outcome} New total: {int(gambling_df.loc[gambling_df.Name == user, "Amount"])}')
        gambling_df.to_csv('gambling.csv', index=False)

@client.command()
async def rps2(ctx, choice='no'):
    pc_choices = ['rock','paper','scissors']
    pc_choice = random.choice(pc_choices)
    if choice not in pc_choices:
        await ctx.send('Invalid Choice')
    elif choice=='no':
        await ctx.send('Try !rps2 rock')
    elif choice == pc_choice:
        await ctx.send(f'{pc_choice}, Tie.')
    elif ((choice == 'paper' and pc_choice == 'scissors') or
         (choice == 'scissors' and pc_choice == 'rock') or
         (choice == 'rock' and pc_choice == 'paper')):
        await ctx.send(f'{pc_choice}, you lose')
    else:
        await ctx.send(f'{pc_choice}, you win')

##############################################################
######## STOCK MARKET COMMANDS ###############################
##############################################################

# now here is where the code starts to get wonky and bad, lol #

import yfinance as yf

def is_market_open():
    import datetime, pytz, holidays
    tz = pytz.timezone('US/Eastern')
    us_holidays = holidays.US()

    now = datetime.datetime.now(tz)
    openTime = datetime.time(hour = 9, minute = 30, second = 0)
    closeTime = datetime.time(hour = 16, minute = 0, second = 0)
    if now.strftime('%Y-%m-%d') in us_holidays: #if holiday
        return False
    if (now.time() < openTime) or (now.time() > closeTime): #if <9:30am or > 4:00pm
        return False
    if now.date().weekday() > 4: #if weekend
        return False

    return True

@client.command()
async def buy(ctx, ticker, shares):
    if is_market_open():
        user = str(ctx.author) #grab author of message
        shares = int(shares)
        gambling_df = pd.read_csv('gambling.csv') #TODO; make sure shares > 0
        tickerData = yf.Ticker(ticker)

        ##############
        stock_df = tickerData.history(period='1d', interval='90m') #this line is breaking it
        #############

        close_price = round(float(stock_df.iloc[-1].Close), 2) #grab recent close price
        user_money = int(gambling_df[gambling_df.Name == user].Amount) #change this to grab name of user.

        if close_price * shares > user_money:
            await ctx.send("You don't have enough money to buy that amount of shares.")

        elif shares <= 0:
            await ctx.send('Enter positive amount of shares.')

        else:
            t_equity = round(close_price * shares, 2)
            await ctx.send(f'Bought {shares} shares at ${close_price} each, for total of ${t_equity}.')
            gambling_df.loc[gambling_df.Name == user, 'Amount'] -= t_equity #subtract equity from total money
            user_df = pd.read_csv(user + '.csv')
            user_df = user_df.append({'Ticker':ticker,'Shares':shares,'Price':close_price,'Total':t_equity}, ignore_index=True)

            average_price = user_df.groupby('Ticker')['Price'].mean() #groupby ticker, find avg price, total price, total shares
            total_cost = user_df.groupby('Ticker')['Total'].sum()
            total_shares = user_df.groupby('Ticker')['Shares'].sum()
            user_df = pd.DataFrame([total_shares, average_price, total_cost]).T
            user_df.to_csv(user + '.csv')
            gambling_df.to_csv('gambling.csv', index=False)
    else:
        await ctx.send('Market is closed!')

@client.command()
async def sell(ctx, ticker, shares):
    if is_market_open():
        user = str(ctx.author)
        shares = int(shares)
        gambling_df = pd.read_csv('gambling.csv')
        user_df = pd.read_csv(user + '.csv')

        tickerData = yf.Ticker(ticker)
        stock_df = tickerData.history(period='1d', interval='90m')
        close_price = round(float(stock_df.iloc[-1].Close), 2)
        sell_value = round(shares * close_price, 2)

        if shares <= 0:
            await ctx.send('Enter positive amount of shares.')

        elif len(user_df[user_df.Ticker == ticker]) > 0: #if ticker exists in user's shares

            if shares > int(user_df.loc[user_df.Ticker==ticker, 'Shares']):
                await ctx.send("You don't have that many shares.")
            else:
                sell_value = shares * close_price
                user_df.loc[user_df.Ticker==ticker, 'Total'] -= shares * float(user_df.loc[user_df.Ticker==ticker, 'Price'])

                user_df.loc[user_df.Ticker==ticker, 'Shares'] -= shares
                gambling_df.loc[gambling_df.Name == user, 'Amount'] += sell_value
                await ctx.send(f'Sold {shares} shares at ${close_price} each, for total of ${sell_value}.')

            user_df.to_csv(user + '.csv', index=False)
            gambling_df.to_csv('gambling.csv', index=False)
        else:
            await ctx.send("You don't own any shares of that ticker.")
    else:
        await ctx.send('Market is closed!')

@client.command()
async def mystocks(ctx):
    user = str(ctx.author)
    await ctx.send(pd.read_csv(user + '.csv'))

@client.command()
async def stockhelp(ctx):
    embed = discord.Embed(title='Stock Commands help')
    embed.add_field(name='!buy {ticker} {#shares}', value='Buy Stock with your gambling winnings.')
    embed.add_field(name='!sell {ticker} {#shares}', value='Sell Stock that you own, goes towards gambling winnings.')
    embed.add_field(name='!mystocks', value='Shows all of your current stocks and the price you bought them at.')
    await ctx.send(embed=embed)

#client.run('Enter Secret Key Here')
