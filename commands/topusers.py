import sqlite3
import discord
from discord.utils import find
import datetime
from config.config import EMBED_COLOUR, EMBED_URL
from operator import itemgetter

def topusers(month, channel, conn):
    # command that displays the top users of the given month in terms of game time

    
    cursor = conn.execute('select ID from '+month) # get all user ids
    users = [user[0] for user in cursor.fetchall()]

    cursor = conn.execute('select * from '+month)
    games = [game[0] for game in cursor.description] #get list of games
    games.pop(0) 

    totals = [0]*len(users)
    
    # sums up the times for each user
    for i in range(len(users)): 
        for game in games:
            cursor = conn.execute('select '+game+' from '+month+' where ID = '+users[i])
            totals[i] += cursor.fetchone()[0] 
        
        
    totals = map(lambda x: x/3600, totals) # converts all the times into hours

    user_totals = list(zip(users,totals))
    user_totals = [i for i in user_totals if i[0] != "Spotify" ] # remove spotify
    user_totals = sorted(user_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order
    user_totals = user_totals[:10] # only displays top ten

    print(user_totals)
    
    
    title = "Top %s gamers in %s:\n" % ("10", month.lower())
 

    #begin constructing message
    i = 1
    content = ""
    for user_id, total in user_totals:
        name = get_name(user_id, channel.guild)

        if name == None:
            return discord.Embed(title=title, type="rich", description=content, colour=EMBED_COLOUR)
        content += '%d: %s - {0:.2f} hours\n\n'.format(total) % (i, str(name))
        i += 1
    
    message = discord.Embed(title=title, type="rich", description=content, colour=EMBED_COLOUR)

    return message


def get_name(id, guild):
    for member in guild.members:
        if str(id) == str(member.id):
            return member.name
