import steamapi
import struct

from binascii import unhexlify

API_KEY = ''
APPID = '250900'

if __name__ == '__main__':
    # api = steamapi.core.APIConnection(api_key=API_KEY)
    # me = steamapi.user.SteamUser(userurl='eur0pa')
    # print me.name
    # print me.steamid
    # print me.profile_url

    today = steamapi.leaderboard.Leaderboard(APPID)
    # today's winner
    # print today
    # or print today.winner

    # winner's profile
    api = steamapi.core.APIConnection(api_key=API_KEY)
    winner = steamapi.user.SteamUser(today.winner['steamid'])

    print "today's winner is {winner} with {points} points!".format(
        winner=winner.name,
        points=today.winner['score'])

    # today's cheater
    # print today.cheater

    # tday's leaderboard id
    # print today.lbid

    # amount of entries
    # print today.entries

    # amount of clean entries in the array
    # print today.clean_entries

    # today's clean ladder
    # print today.clean_leaderboard

    # today's vanilla ladder
    # print today.leaderboard
