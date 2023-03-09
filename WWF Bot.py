import discord
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
import time
import requests

def get_ipa(string):

    source = requests.get('http://showmeword.com/definition/english_word/' + string).text
    soup = BeautifulSoup(source, 'lxml')
    match = soup.find('div', class_='trans_sound')
    bettermatch = match.find('span', class_='transcription')
    bettermatch = str(bettermatch)
    bettermatch = bettermatch.split("|", 1)[1]
    return bettermatch.split("|", 1)[0]


def get_song(string):
    s = string.replace(" ", "%20")
    source = requests.get('https://www.lyrics.com/lyrics/' + s).text
    soup = BeautifulSoup(source, 'lxml')
    match = soup.find('div', class_='lyric-meta within-lyrics fll')
    title = match.find('p', class_='lyric-meta-title')
    title = str(title)
    title = title[43:]
    title = title.split(">", 1)[1]
    title = title.split("<")[0]
    artist = match.find('p', class_='lyric-meta-album-artist')
    artist = str(artist)
    artist = artist.split(">")[2]
    artist = artist.split("<")[0]
    result = "" + title + " by " + artist

    return result



def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def score(string):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    numbers = [1,4,4,2,1,4,3,3,1,10,5,2,4,2,1,4,10,1,1,1,2,5,4,8,3,10]
    sum = 0
    string = string.lower()
    for c in string:
        index = letters.index(c)
        sum = sum + numbers[index]
    return sum

token = read_token()

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):

    if message.content.startswith('.pts'):
        args = message.content.split(" ")
        try:
            if len(args) != 2:
                await message.channel.send("The pts command takes in 1 word.")
            else:
                pts = score(args[1])
                result = str(args[1]) + " = " + str(pts) + " points"
                await message.channel.send(result)
        except:
            await message.channel.send("Something went wrong :(")

    if message.content.startswith('.most'):
        args = message.content.split(" ")
        try:
            if len(args) != 3 and len(args) != 4:
                await message.channel.send("The most command takes in 2 or 3 words.")
            if len(args) == 3:
                scores1 = [score(args[1]), score(args[2])]
                if scores1[0] == scores1[1]:
                    await message.channel.send("Tie between " + str(args[1]) + " and " + str(args[2]))
                else:
                    max_2 = max(scores1)
                    j = scores1.index(max_2)
                    await message.channel.send(str(args[j+1]) + " is worth the most points")

            else:
                scores = [score(args[1]), score(args[2]), score(args[3])]
                if scores[0] != scores[1] and scores[0] != scores[2]:
                    max_pts = max(scores)
                    i = scores.index(max_pts)
                    await message.channel.send(args[i + 1] + " is worth the most points")
                elif scores[0] == scores[1] and scores[0] != scores[2]:
                    if scores[2] > scores[1]:
                        await message.channel.send(args[3])
                    else:
                        await message.channel.send("Tie between " + args[1] + " and " + args[2])
                elif scores[0] == scores[2] and scores[0] != scores[1]:
                    if scores[1] > scores[0]:
                        await message.channel.send(args[2])
                    else:
                        await message.channel.send("Tie between " + args[1] + " and " + args[3])
                elif scores[1] == scores[2] and scores[1] != scores[0]:
                    if scores[0] > scores[1]:
                        await message.channel.send(args[1])
                    else:
                        await message.channel.send("Tie between " + args[2] + " and " + args[3])
#                elif scores[0] == scores[1] and scores[1] == scores[2]:
                else:
                    await message.channel.send("All three have the same point value.")
        except:
            await message.channel.send("Something went wrong :(")

    if message.content.startswith('.ipa'):
        try:
            args = message.content.split(" ")
            ipa = get_ipa(args[1])
            await message.channel.send("IPA form = " + ipa)
        except:
           await message.channel.send("An error occurred. Is the word real? Did you put in more than one word?")

    if message.content.startswith('.oot'):
        try:
            s = message.content.replace(".oot ", "")
            await message.channel.send(get_song(s))
        except:
            await message.channel.send("Something went wrong :(")

    if message.content.startswith('.all'):
        try:
            args = message.content.split(" ")
            if len(args) == 4:
                pts1 = score(args[1])
                pts2 = score(args[2])
                pts3 = score(args[3])
                await message.channel.send("" + args[1] + " = " + str(pts1) + " points" + "\n" + args[2] + " = " + str(pts2) + " points" + "\n" + args[3] + " = " + str(pts3) + " points")
            elif len(args) == 3:
                pts_1 = score(args[1])
                pts_2 = score(args[2])
                await message.channel.send("" + args[1] + " = " + str(pts_1) + " points" + "\n" + args[2] + " = " + str(pts_2) + " points")
        except:
            await message.channel.send("Something went wrong :(")

client.run(token)
