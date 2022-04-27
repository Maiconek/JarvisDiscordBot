import discord
import requests
from requests import get
from discord.ext import commands
from datetime import date
import datetime

TOKEN = #token for your bot

API_KEY = #Personal API Key for weather informations
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

NBA_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

QUOTE_URL = "https://quotes.rest/qod?language=en"

quote_request = requests.get(QUOTE_URL)


request_url = f"{BASE_URL}?appid={API_KEY}&q=Gdynia"

response = requests.get(request_url)

client = discord.Client()

@client.event
async def on_ready():
    print("{0.user} is online!".format(client))

def get_links():
    data = get(NBA_URL + ALL_JSON).json()
    links = data['links']
    return links
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("!weather") or message.content.startswith("!pogoda"):
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = round(data["main"]["temp"] - 273.15, 2)
            wind = data['wind']['speed']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']

            await message.channel.send("**Currently in Gdynia:** " + weather)
            await message.channel.send("**Temperature:** " + str(temperature) + " ℃")
            await message.channel.send("**Wind speed:** " + str(wind) + " km/h")
            await message.channel.send("**Humidity:** " + str(humidity) + " %")
            await message.channel.send("**Pressure:** " + str(pressure) + " hPa")
        else:
            await message.channel.send("Error")
    
    elif message.content.startswith("!help") or message.content.startswith("!pomoc"):
        await message.channel.send("Available commands:")
        await message.channel.send("!help --- well you already know this one")
        await message.channel.send("!whoami --- I am gonna introduce myself and tell you what am I actually doing")
        await message.channel.send("!date --- I am going to tell you todays date")
        await message.channel.send("!weather --- I will tell you about current weather in city of Gdynia")
        await message.channel.send("!nba --- I will show you current standings in both west and east division")
        await message.channel.send("!joke --- I am gonna tell you a joke. Just to let you know I'm a big comedian hehehe")
        await message.channel.send("!quote --- I will tell you what is the quote of a day")


    elif message.content.startswith("!whoami"):
        await message.channel.send("My name is Jarvis and I am a discord bot created by Maicon. I was created with purpose to make discord servers great again! I have got a lot of diffrent functionalities. Also my creator is constantly adding new features. Make sure you don't miss any of them!")
    
    elif message.content.startswith("!nba"):
        standings = get_links()['leagueConfStandings']
        data = get(NBA_URL + standings).json()['league']['standard']['conference']['east']
    
        await message.channel.send("**EASTERN CONFERENCE STANDINGS**")
        for team in data:
            name = team['teamSitesOnly']['teamName']
            nick = team['teamSitesOnly']['teamNickname']
            win = "Wins: " + team['win']
            loss = "Losses: " + team['loss']
            rank = str(team['confRank']) + ". "
            
            await message.channel.send(rank + name + " " + nick + " " + win + " " + loss)
            #await message.channel.send(nick)
        data2 = get(NBA_URL + standings).json()['league']['standard']['conference']['west']

        await message.channel.send("--------------------")
        await message.channel.send("**WESTERN CONFERENCE STANDINGS**")
        for team in data2:
            name = team['teamSitesOnly']['teamName']
            nick = team['teamSitesOnly']['teamNickname']
            win = "Wins: " + team['win']
            loss = "Losses: " + team['loss']
            rank = str(team['confRank']) + ". "
            await message.channel.send(rank + name + " " + nick + " " + win + " " + loss)


    elif message.content.startswith("!joke"):
        r = requests.get('https://sv443.net/jokeapi/v2/joke/Miscellaneous,Pun,Spooky,Christmas?blacklistFlags=nsfw,racist,sexist&type=single').json()
        joke = r['joke']
        await message.channel.send(joke)

    elif message.content.startswith("!quote"):
        if quote_request.status_code == 200:
            data = get(QUOTE_URL).json()['contents']['quotes']
    
            for i, j in zip(data, data):
                author = i['author']
                currentDate = i['date']
                quote = j['quote']
                title = j['title']
    
            await message.channel.send(title + " of " + currentDate + ".")
            await message.channel.send(quote)  
            await message.channel.send("Author: " + author)
        else:
            await message.channel.send("Error")
    
    elif message.content.startswith("!date"):
        temp = date.today()
        today = temp.strftime('%d %B %Y')
        
        await message.channel.send("Today is " + today)
    
    
client.run(TOKEN)