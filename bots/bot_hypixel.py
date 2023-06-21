from .lib.bot_hypixel import BotHypixel
from .lib import langs
from .lib.utils import *

MAP_PREFIX_COLOR = {
    'GOLD': '金色',
    'AQUA': '青色'
}

MAP_PLUS_COLOR = {
    'RED': '浅红色 (默认)',
    'GOLD': '金色 (35 级)',
    'GREEN': '浅绿色 (45 级)',
    'YELLOW': '黄色 (55 级)',
    'LIGHT_PURPLE': '粉色 (65 级)',
    'WHITE': '白色 (75 级)',
    'BLUE': '浅蓝色 (85 级)',
    'DARK_GREEN': '深绿色 (95 级)',
    'DARK_RED': '深红色 (150 级)',
    'DARK_AQUA': '青色 (150 级)',
    'DARK_PURPLE': '紫色 (200 级)',
    'DARK_GRAY': '灰色 (200 级)',
    'BLACK': '黑色 (250 级)',
    'DARK_BLUE': '深蓝色 (100 Rank)'
}

def exp_to_level(exp):
    return (0.0008 * exp + 12.25) ** 0.5 - 2.5

def get_rank_color_line(player):
    g = get_getter(player, None)
    rank = get_raw_rank(player)
    prefix_color = g('monthlyRankColor', 'GOLD')
    prefix_color = MAP_PREFIX_COLOR.get(prefix_color, prefix_color)
    plus_color = g('rankPlusColor', 'RED')
    plus_color = MAP_PLUS_COLOR.get(plus_color, plus_color)
    if rank == 'MVP_PLUS':
        return '\nMVP+ 颜色: %s' % plus_color
    elif rank == 'SUPERSTAR':
        return '\nMVP 颜色: %s | ++ 颜色: %s' % (prefix_color, plus_color)
    return ''

def parser(args, settings, *_):
    require(len(args) == 1, langs.ERROR_ARGUMENT)
    player = get_player_by_username(args[0], settings)
    g = get_getter(player, 0)
    ga = get_getter(get(player, 'achievements'), 0)
    return f'{get_name(player)} 的 Hypixel 信息:'\
            + '\n等级: %.3f | 人品: %d' % (exp_to_level(g('networkExp')), g('karma'))\
            + get_rank_color_line(player)\
            + '\n成就点数: %d | 赠送 Rank: %d' % (g('achievementPoints'), g('giftingMeta.ranksGiven'))\
            + '\n完成任务: %d | 完成挑战: %d' % (ga('general_quest_master'), ga('general_challenger'))\
            + '\n小游戏胜场: %d | 获得硬币: %d' % (ga('general_wins'), ga('general_coins'))\
            + '\n活动银币: %d | 锦标赛战魂: %d' % (g('seasonal.silver'), g('tourney.total_tributes'))\
            + optional(g('userLanguage', None), '\n使用语言: %s' % (to_camel(g('userLanguage'))))\
            + optional(g('firstLogin', None), '\n首次登录: %s' % (time_to_string_ms(g('firstLogin'))))\
            + optional(g('lastLogin', None), '\n上次登录: %s' % (time_to_string_ms(g('lastLogin'))))\
            + optional(g('lastLogout', None), '\n上次退出: %s' % (time_to_string_ms(g('lastLogout'))))\
            + optional(g('mostRecentGameType', None), '\n最近游玩: %s' % (to_camel(g('mostRecentGameType'))))\
            + name_diff(args[0], player)


bot = BotHypixel('hypixel', 'hyp', parser)
