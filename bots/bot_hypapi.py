from .lib.bot_hypixel import BotHypixel
from .lib.bot_error import BotException
from .lib import langs
from .lib.utils import *


def parser(args, settings, *_):
    require(len(args) == 2 or len(args) == 3, langs.ERROR_ARGUMENT)
    player = get_player_by_username(args[0], settings)
    g = get_getter(player, None)
    value = None
    try:
        value = g(args[1])
    except Exception:
        raise BotException(langs.ERROR_QUERY)
    if value is None:
        raise BotException('值不存在!')
    value_str = '%s 的 Hypixel API:\n位置: %s' % (get_name(player), args[1])
    if isinstance(value, dict):
        value_str += '\n类型: 对象\n长度: %d' % len(value)
        if len(args) == 3:
            if args[2] in value:
                value_str += '\n对象包含键 %r' % args[2]
            else:
                value_str += '\n对象不包含键 %r' % args[2]
    elif isinstance(value, list):
        value_str += '\n类型: 列表\n长度: %d' % len(value)
        if len(args) == 3:
            if args[2] in value:
                value_str += '\n列表包含值 %r' % args[2]
            else:
                value_str += '\n列表不包含值 %r' % args[2]
    elif isinstance(value, str):
        value_str += '\n类型: 字符串\n长度: %d\n值: %r' % (len(value), value[:100])
    elif isinstance(value, bool):
        value_str += '\n类型: 布尔值\n值: %s' % value
    elif isinstance(value, int):
        value_str += '\n类型: 整数\n值: %d' % value
    elif isinstance(value, float):
        value_str += '\n类型: 浮点数\n值: %f' % value
    else:
        value_str += '\n类型: 其它类型 (%s)' % (value, type(value))
    return value_str + name_diff(args[0], player)


bot = BotHypixel('hypapi', 'hypapi', parser)
