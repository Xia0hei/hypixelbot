from .lib.bot_hypixel import BotHypixel
from .lib import langs
from .lib.utils import *


MODE_MAP = {}


def register(prefix, description, *aliases):
    for alias in aliases:
        MODE_MAP[alias] = (prefix, description)


def register_dream(name, description, short):
    register(f'eight_two_{name}_', f'双人{description}模式',
             f'eight_two_{name}', f'{short}2', f'8_2_{name}')
    register(f'four_four_{name}_', f' 4v4v4v4 {description}模式',
             f'four_four_{name}', f'{short}4', f'4_4_{name}')


register('', '', '', 'all', 'a', 'overall')
register('eight_one_', '单人模式', 'eight_one',
         'solo', 'solos', '1', '1s', '81', '1v1', '8_1')
register('eight_two_', '双人模式', 'eight_two',
         'double', 'doubles', '2', '2s', '82', '2v2', '8_2')
register('four_three_', ' 3v3v3v3 ', 'four_three', 'three',
         'threes', '3', '3s', '43', '3v3', '3v3v3v3', '3333', '4_3')
register('four_four_', ' 4v4v4v4 ', 'four_four',
         'four', 'fours', '4', '4s', '44', '4v4v4v4', '4444', '4_4')
register('two_four_', ' 4v4 ', 'two_four', '4v4', '24', '2_4')
register('castle_', ' 40v40 城池攻防战模式', 'castle',
         'two_forty', '40', '240', '40v40')
register_dream('voidless', '无虚空', 'v')
register_dream('armed', '枪战', 'a')
register_dream('swap', '交换', 's')
register_dream('rush', '疾速', 'r')
register_dream('ultimate', '超能力', 'u')
register_dream('lucky', '幸运方块', 'l')
register_dream('underworld', 'Underworld', 'uw')


def get_bedwars_stars(exp):
    level = 100 * (exp // 487000)
    exp %= 487000
    if exp < 500:
        return level, exp, '500'
    if exp < 1500:
        return level + 1, exp - 500, '1k'
    if exp < 3500:
        return level + 2, exp - 1500, '2k'
    if exp < 7000:
        return level + 3, exp - 3500, '3.5k'
    return level + 4 + (exp - 7000) // 5000, (exp - 7000) % 5000, '5k'

def get_bedwars_star_char(stars):
    if stars < 1100:
        return '\u272b'
    elif stars < 2100:
        return '\u272a'
    else:
        return '\u269d'

def parser(args, settings, *_):
    require(len(args) == 1 or len(args) == 2, langs.ERROR_ARGUMENT)
    mode = MODE_MAP.get('' if len(args) == 1 else args[1], None)
    require(mode is not None, f'未知的模式: {"" if len(args) == 1 else args[1]}!')
    player = get_player_by_username(args[0], settings)
    g = get_getter(get(player, 'stats.Bedwars'), 0)
    stars, exp, full = get_bedwars_stars(int(g('Experience')))
    star = get_bedwars_star_char(stars)
    return f'[{stars}{star}] {get_name(player)} 的起床战争{mode[1]}数据:'\
            + '\n经验: %d/%s | 硬币: %d' % (exp, full, g('coins'))\
            + optional(g(mode[0] + 'winstreak', None), ' | 连胜: %d' % g(mode[0] + 'winstreak'))\
            + '\n拆床: %d | 被拆床: %d | BBLR: %s' % ratio(g(mode[0] + 'beds_broken_bedwars'), g(mode[0] + 'beds_lost_bedwars'))\
            + '\n胜场: %d | 败场: %d | W/L: %s' % ratio(g(mode[0] + 'wins_bedwars'), g(mode[0] + 'losses_bedwars'))\
            + '\n击杀: %d | 死亡: %d | K/D: %s' % ratio(g(mode[0] + 'kills_bedwars'), g(mode[0] + 'deaths_bedwars'))\
            + '\n终杀: %d | 终死: %d | FKDR: %s' % ratio(g(mode[0] + 'final_kills_bedwars'), g(mode[0] + 'final_deaths_bedwars'))\
            + '\n收集铁锭: %d | 收集金锭: %d' % (g(mode[0] + 'iron_resources_collected_bedwars'), g(mode[0] + 'gold_resources_collected_bedwars'))\
            + '\n收集钻石: %d | 收集绿宝石: %d' % (g(mode[0] + 'diamond_resources_collected_bedwars'), g(mode[0] + 'emerald_resources_collected_bedwars'))\
            + name_diff(args[0], player)


bot = BotHypixel('bedwars', 'bw', parser)
