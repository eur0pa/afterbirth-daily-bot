import greedbuttapi

if __name__ == '__main__':

    today = greedbuttapi.leaderboard.Leaderboard()

    print "today's winner is {winner} with {points} points!".format(
        winner=(today.winner['name']).encode('utf8'),
        points=today.winner['score'])

