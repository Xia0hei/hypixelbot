from .lib.bot_hypixel import BotHypixel
from .lib import langs
from .lib.utils import *


LEVEL_EXPS = (
    (20, '20'),
    (50, '50'),
    (80, '80'),
    (100, '100'),
    (250, '250'),
    (500, '500'),
    (1000, '1k'),
    (1500, '1.5k'),
    (2500, '2.5k'),
    (4000, '4k'),
    (5000, '5k'),
    (10000, '10k')
)


def add_3(a, b, c):
    return a + b + c, a, b, c


def parser(args, settings, *_):
    require(len(args) == 1, langs.ERROR_ARGUMENT)
    player = get_player_by_username(args[0], settings)
    g = get_getter(get(player, 'stats.SkyWars'), 0)
    total_exp = g('skywars_experience')
    exp, full = 0, '0'
    if total_exp >= 15000:
        exp = (total_exp - 15000) % 10000
        full = '10k'
    else:
        total_level_exp = 0
        for level_exp, level_exp_name in LEVEL_EXPS:
            total_level_exp += level_exp
            if total_exp >= total_level_exp:
                exp = total_exp - total_level_exp
            else:
                full = level_exp_name
                break
    stars = reset_style(g('levelFormatted', '0\u22c6'))
    return f'[{stars}] {get_name(player)} 的空岛战争数据:'\
            + '\n经验: %d/%s | 连胜: %s' % (exp, full, g('win_streak'))\
            + '\n时空漩涡: %d%%=%d%%+%d%%+%d%%' % add_3(g('angel_of_death_level'), g('angels_offering'),
                1 if 'favor_of_the_angel' in g('packages', []) else 0)\
            + '\n硬币: %d | 代币: %d' % (g('coins'), g('cosmetic_tokens'))\
            + '\n欧泊: %d | 欧泊碎片: %d/1.5k' % (g('opals'), g('shard'))\
            + '\n击杀: %d | 死亡: %d | K/D: %s' % ratio(g('kills'), g('deaths'))\
            + '\n胜场: %d | 败场: %d | W/L: %s' % ratio(g('wins'), g('losses'))\
            + '\n灵魂: %d | 头颅: %d | 助攻: %d' % (g('souls'), g('heads'), g('assists'))\
            + name_diff(args[0], player)


bot = BotHypixel('skywars', 'sw', parser)
