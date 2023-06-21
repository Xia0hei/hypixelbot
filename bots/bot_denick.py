from .lib.bot_hypixel import BotHypixel
from .lib.bot_error import BotException
from .lib import langs
from .lib.utils import *


def parser(args, settings, *_):
    require(len(args) == 1, langs.ERROR_ARGUMENT)
    denick = denick_by_username(args[0], settings)
    g = get_getter(denick)
    if g('nick_in_pool'):
        return f'{g("ign")} -> {g("latest_nick")}'\
                + '\n查询的 Nick: %s' % g('queried_nick')\
                + '\nDenick 时间: %s' % time_to_string(g('first_detected'))\
                + '\n上次发现: %s' % time_to_string(g('last_seen'))
    else:
        raise BotException('Nick 不存在!')


bot = BotHypixel('denick', 'denick', parser)
