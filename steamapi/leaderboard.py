import urllib2
import simplexml
import datetime

from .decorators import cached_property, MINUTE, HOUR

__author__ = 'europa'


class Leaderboard(object):
    URL_BASE = 'http://steamcommunity.com'

    def __init__(self, appid=None, date=None, lbid=None, start=0, end=250):
        self._appid = appid
        self._lbid = lbid
        self._date = date
        self._start = start
        self._end = end

        if appid is None:
            raise ValueError('gameid is needed')

        if self._lbid is None:
            # retrieve the latest leaderboard id
            self._lbid = self._get_leaderboard_id()

        self._entries = self._get_leaderboard_entries()
        self._clean_entries = self._get_clean_leaderboard_entries()

    # overrides
    def __str__(self):
        return str(repr(self.winner))

    @cached_property(ttl=30 * MINUTE)
    def winner(self):
        return self._clean_entries[0]

    @cached_property(ttl=30 * MINUTE)
    def cheater(self):
        return self._entries[0]

    @cached_property(ttl=12 * HOUR)
    def lbid(self):
        return self._lbid

    @cached_property(ttl=30 * MINUTE)
    def clean_entries(self):
        return self._total_clean_entries

    @cached_property(ttl=30 * MINUTE)
    def entries(self):
        return self._total_entries

    @cached_property(ttl=30 * MINUTE)
    def leaderboard(self):
        return self._entries

    @cached_property(ttl=30 * MINUTE)
    def clean_leaderboard(self):
        return self._clean_entries

    def _get_leaderboard_id(self):
        if self._date is None:
            date = datetime.date.today().strftime('%Y%m%d')

        board_name = date + '_scores'

        url = '{base}/stats/{appid}/leaderboards/?xml=1'.format(
            base=self.URL_BASE,
            appid=self._appid)
        try:
            r = urllib2.urlopen(url)
        except Exception:
            raise

        xml = r.read()
        data = simplexml.loads(xml)

        for board in data['response']['leaderboard']:
            if board['name'] == board_name:
                if board['entries'] < 100:
                    self._date = (
                        datetime.date.today() -
                        datetime.timedelta(1).strftime(
                        '%Y%m%d'))
                    self._lbid = self._get_leaderboard_id()

                return board['lbid']

    def _get_leaderboard_entries(self):
        url = '{base}/stats/{appid}/leaderboards/{lbid}/?xml=1&start={start}&end={end}'.format(
            base=self.URL_BASE,
            appid=self._appid,
            lbid=self._lbid,
            start=self._start,
            end=self._end)
        try:
            r = urllib2.urlopen(url)
        except Exception:
            raise

        xml = r.read()
        data = simplexml.loads(xml)['response']

        self._total_entries = int(data['totalLeaderboardEntries'])

        tmp = []
        for entry in data['entries']:
            try:
                # handle single entries
                if entry['steamid']:
                    pass
            except TypeError:
                entry = data['entries']['entry']

            tmp.append({
                'rank': int(entry['rank']),
                'score': int(entry['score']),
                'steamid': entry['steamid'],
                'details': entry['details']})

        return tmp

    def _get_clean_leaderboard_entries(self):
        clean = []
        for entry in self._entries:
            tmp = []

            details = entry['details']
            details = [details[i:i+8] for i in range(0, len(details), 8)]

            for score in details:
                tmp.append(self.swap32(int(score, 16)))

            try:
                if ((tmp[1] > tmp[0]) or            # schwag > stage
                    (tmp[9] > tmp[0]) or            # item penalty > stage
                    (tmp[12] > 0 and                # unk_13 > 0 &&
                     tmp[12] < entry['score']) or   # score > unk_13
                    (tmp[6] > 25000)):              # exp.bonus > 25k
                    continue
            except:
                pass

            clean.append(entry)

        self._total_clean_entries = len(clean)
        return clean

    def swap32(self, x):
        return (((x << 24) & 0xFF000000) |
                ((x <<  8) & 0x00FF0000) |
                ((x >>  8) & 0x0000FF00) |
                ((x >> 24) & 0x000000FF))
