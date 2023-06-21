import json
import requests
import json
import re
import time
from . import langs
from .cooldown import Cooldown
from .bot_error import BotException

CUSTOM_RANKS = {
    'a77d4929684e4308b326e37b58e1e4f4': '[YOUTUBE] ',
    'cb9013f60bec4f9e9186769ca4e188fb': '[YOUSHABER] ',
    '8630fc523c7740e1aa7bff0b223ebe36': '[Q_TT] ###',
    'f8d015cbc2114b67b692497db1d7aaea': '[Q_TT] ###',
    '0b5a85ba81a1424f98695ca3e006a6ce': '[Q_TT] ###',
    '8473f4ff81244f07b7d7585bee70118d': '[Q_TT] ###',
    '9c41a904740d4075ba05bcda28acd5c9': '[Q_TT] ###',
    'e8fa5672450842ad8ed61feb7e897370': '[Q_TT] ###',
    'd26084f69f9a4779a033c83ab707129f': '[Q_TT] ###',
    '3806b939101d4dbaa3ca13ed88601624': '[LLL] ###',
    '84582afc65c0475cbfa65c151acdaa5e': '[DICKLONG] ###',
    '78f2942621c44b71b9545669d00fd094': '[DICKSHORT] ###',
    '1c1cbcd2aec4427ba87cbcd7e4721f61': '[帅哥] [大神] [DICKLONG] [YOUTUBE] ',
    'c24b9f01b9d74804b98bb6b515a36d95': '[帅哥] [大神] [DICKLONG] [YOUTUBE] ',
    '326b7d2255de41e2aac0c268d9561340': '[大神] ###'
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

HPIXEL_API_KEY = ''
ANTISNIPER_API_KEY = ''
COOLDOWN = Cooldown(1.0)

RE_STYLE = re.compile(r'\u00a7.')
RE_USERNAME = re.compile(r'^([a-z0-9_]{1,16}|[a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$')

URL_API_MOJANG = 'https://api.mojang.com/users/profiles/minecraft/%s'
URL_API_HYPIXEL_PLAYER = f'https://api.hypixel.net/player?key={HPIXEL_API_KEY}&uuid=%s'
URL_API_HYPIXEL_STATUS = f'https://api.hypixel.net/status?key={HPIXEL_API_KEY}&uuid=%s'
URL_API_ANTISNIPER_DENICK = f'https://api.antisniper.net/denick?key={ANTISNIPER_API_KEY}&nick=%s'
URL_API_ANTISNIPER_FINDNICK = f'https://api.antisniper.net/findnick?key={ANTISNIPER_API_KEY}&name=%s'

MAP_RANK = {
    'ADMIN': '[ADMIN] ',
    'GAME_MASTER': '[GM] ',
    'YOUTUBER': '[YOUTUBE] ',
    'SUPERSTAR': '[MVP++] ',
    'VIP': '[VIP] ',
    'VIP_PLUS': '[VIP+] ',
    'MVP': '[MVP] ',
    'MVP_PLUS': '[MVP+] ',
}

def get_json(url, settings={}):
    if get(settings, "global.api_cdn", False):
        url = url.replace('api.hypixel.net', 'api.hypixel.gcorecdn.ouralioth.com')
        url = url.replace('api.antisniper.net', 'api.antisniper.gcorecdn.ouralioth.com')
    return json.loads(requests.get(url, headers={'User-Agent': USER_AGENT}).content.decode('utf-8'))

def check_username(username):
    if not RE_USERNAME.match(username):
        raise BotException(langs.ERROR_USERNAME)

def get_uuid(username):
    username = username.replace('-', '_')
    username = username.lower()
    check_username(username)
    if len(username) > 16:
        return username
    return get_json(URL_API_MOJANG % username)['id']

def get_player(uuid, settings):
    return get_json(URL_API_HYPIXEL_PLAYER % uuid, settings)

def get_status(uuid, settings):
    return get_json(URL_API_HYPIXEL_STATUS % uuid, settings)

def get_player_by_username(username, settings):
    COOLDOWN.wait()
    return get(get_player(get_uuid(username), settings), 'player')

def get_status_by_username(username, settings):
    COOLDOWN.wait()
    return get(get_status(get_uuid(username), settings), 'session')

def denick_by_username(username, settings):
    username = username.replace('-', '_')
    COOLDOWN.wait()
    check_username(username)
    return get(get_json(URL_API_ANTISNIPER_DENICK % username, settings), 'player')

def findnick_by_username(username, settings):
    username = username.replace('-', '_')
    COOLDOWN.wait()
    check_username(username)
    return get(get_json(URL_API_ANTISNIPER_FINDNICK % username, settings), 'player')

def reset_style(string):
    return ''.join(RE_STYLE.split(string))

def get(player, path, default=None):
    try:
        if player is None:
            return default
        index_list = path.split('.')
        current = player
        for index in index_list:
            current = current.get(index, None)
            if current is None:
                return default
        return current
    except Exception:
        pass
    return default

def get_getter(player, default_value=None):
    def _getter(path, default=default_value):
        return get(player, path, default)
    return _getter

def _get_rank(player):
    g = get_getter(player)
    rank_prefix = g('prefix')
    if rank_prefix:
        return reset_style(rank_prefix) + ' '
    rank_rank = g('rank')
    if rank_rank in MAP_RANK:
        return MAP_RANK[rank_rank]
    rank_monthly = g('monthlyPackageRank')
    if rank_monthly in MAP_RANK:
        return MAP_RANK[rank_monthly]
    rank_new = g('newPackageRank')
    if rank_new in MAP_RANK:
        return MAP_RANK[rank_new]
    rank_package = g('packageRank')
    if rank_package in MAP_RANK:
        return MAP_RANK[rank_package]
    return ''

def get_rank(player):
    g = get_getter(player)
    rank = _get_rank(player)
    rank_custom = g('uuid')
    if rank_custom in CUSTOM_RANKS:
        return CUSTOM_RANKS[rank_custom].replace('###', rank)
    return rank

def get_raw_rank(player):
    g = get_getter(player)
    rank_prefix = g('prefix')
    if rank_prefix:
        return 'CUSTOM'
    rank_rank = g('rank')
    if rank_rank in MAP_RANK:
        return rank_rank
    rank_monthly = g('monthlyPackageRank')
    if rank_monthly in MAP_RANK:
        return rank_monthly
    rank_new = g('newPackageRank')
    if rank_new in MAP_RANK:
        return rank_new
    rank_package = g('packageRank')
    if rank_package in MAP_RANK:
        return rank_package
    return ''

def get_name(player):
    username = get(player, 'displayname', '???')
    rank = get_rank(player)
    return rank + username

def ratio(valuea, valueb):
    if valueb == 0:
        return valuea, valueb, str(valuea)
    return valuea, valueb, '%.3f' % (valuea / valueb)

def require(condition, error_message):
    if not condition:
        raise BotException(error_message)

def optional(condition, string):
    if condition is not None:
        return string
    return ''

def time_to_string_ms(time_):
    localtime = time.localtime(time_ // 1000)
    return '%d.%d.%d-%d:%02d:%02d.%03d' % (
        localtime.tm_year,
        localtime.tm_mon,
        localtime.tm_mday,
        localtime.tm_hour,
        localtime.tm_min,
        localtime.tm_sec,
        time_ % 1000
    )

def time_to_string(time_):
    localtime = time.localtime(time_)
    return '%d.%d.%d-%d:%02d:%02d.%03d' % (
        localtime.tm_year,
        localtime.tm_mon,
        localtime.tm_mday,
        localtime.tm_hour,
        localtime.tm_min,
        localtime.tm_sec,
        time_ % 1000
    )

def name_diff(name, player):
    name = name.replace('-', '_')
    if len(name) > 16:
        return '\nUUID: ' + name
    if name.lower() != get(player, 'displayname', '???').lower():
        return '\n此玩家已改名! (%s -> %s)' % (get(player, 'displayname', '???'), name)
    return ''

def to_camel(string):
    if not isinstance(string, str):
        return ''
    l = string.split('_')
    r = []
    for s in l:
        s = s[:1].upper() + s[1:].lower()
        r.append(s)
    return ' '.join(r)
