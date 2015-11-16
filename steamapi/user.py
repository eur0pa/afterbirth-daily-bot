import datetime

from .core import APIConnection, SteamObject

from .decorators import cached_property, INFINITE, MINUTE, HOUR
from .errors import *


__author__ = 'SmileyBarry'
# adapted and reduced from https://raw.githubusercontent.com/smiley/steamapi/master/steamapi/user.py


class SteamUser(SteamObject):
    # OVERRIDES
    def __init__(self, userid=None, userurl=None):
        """
        Create a new instance of a Steam user. Use this object to retrieve details about
        that user.

        :param userid: The user's 64-bit SteamID. (Optional, unless steam_userurl isn't specified)
        :type userid: int
        :param userurl: The user's vanity URL-ending name. (Required if "steam_userid" isn't specified,
        unused otherwise)
        :type userurl: str
        :raise: ValueError on improper usage.
        """
        if userid is None and userurl is None:
            raise ValueError("One of the arguments must be supplied.")

        if userurl is not None:
            if '/' in userurl:
                # This is a full URL. It's not valid.
                raise ValueError("\"userurl\" must be the *ending* of a vanity URL, not the entire URL!")
            response = APIConnection().call("ISteamUser", "ResolveVanityURL", "v0001", vanityurl=userurl)
            if response.success != 1:
                raise UserNotFoundError("User not found.")
            userid = response.steamid

        if userid is not None:
            self._id = int(userid)

    def __eq__(self, other):
        if type(other) is SteamUser:
            if self.steamid == other.steamid:
                return True
            else:
                return False
        else:
            return super(SteamUser, self).__eq__(other)

    def __str__(self):
        return self.name

    def __hash__(self):
        # Don't just use the ID so ID collision between different types of objects wouldn't cause a match.
        return hash(('user', self.id))

    # PRIVATE UTILITIES
    @cached_property(ttl=2 * HOUR)
    def _summary(self):
        """
        :rtype: APIResponse
        """
        return APIConnection().call("ISteamUser", "GetPlayerSummaries", "v0002", steamids=self.steamid).players[0]

    # PUBLIC ATTRIBUTES
    @property
    def steamid(self):
        """
        :rtype: int
        """
        return self._id

    @cached_property(ttl=INFINITE)
    def name(self):
        """
        :rtype: str
        """
        return self._summary.personaname

    @cached_property(ttl=INFINITE)
    def real_name(self):
        """
        :rtype: str
        """
        return self._summary.realname

    @cached_property(ttl=INFINITE)  # Already cached, but unlikely to change.
    def profile_url(self):
        """
        :rtype: str
        """
        return self._summary.profileurl
