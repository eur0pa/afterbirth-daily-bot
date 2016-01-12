import urllib2
import json

__author__ = 'europa'


class Leaderboard(object):
    URL_BASE = "https://greedbutt.com"
    PAGE = "index.php"
    PARAMS = "json=true"

    def __init__(self):
        self._entries = self._get_leaderboard_entries()

    def __str__(self):
        return str(repr(self.winner))

    @property
    def winner(self):
        return self._entries[0]

    @property
    def leaderboard(self):
        return self._entries

    def _get_leaderboard_entries(self):
        url = '{base}/{page}?{params}'.format(
            base=self.URL_BASE,
            page=self.PAGE,
            params=self.PARAMS)
        try:
            r = urllib2.urlopen(url)
        except:
            return

        data = json.loads(r.read())

        tmp = []
        for entry in data:
            tmp.append({
                'rank': int(entry['rank']),
                'score': int(entry['score']),
                'name': entry['player']['name']})

        return tmp


if __name__ == '__main__':
    main()
