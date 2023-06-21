from .lib.bot_base import BotBase
from .lib.bot_error import BotException, LOG
import time
import random


def last(*args):
    return args[-1]


def get_time():
    localtime = time.localtime()
    return ((localtime.tm_year * 373 + localtime.tm_yday) * 31 + localtime.tm_hour) * 53 + localtime.tm_min // 5


def get_random(bound):
    r = random.random()
    r *= r
    return int(r * bound)


def adjust(number):
    if number < 50:
        number += random.randint(0, 20)
    elif number >= 80:
        number -= random.randint(0, 10)
    return number


REPLIES = {
    '/luck': lambda x: f'[CQ:at,qq={x}] 你当前的幸运值为%d%%!' % last(
        random.seed(x * 97 + get_time()),
        adjust(int(100 - get_random(11 if x ==
               2087315306 else (51 if x == 2984028717 else 101))))
    ),
    '/yhelp': lambda x:
        'Yqloss 机器人指令列表：\n'
        '/hyp <ID> 查询 Hypixel 信息\n'
        '/bw <ID> [模式] 查询起床战争数据\n'
        '/sw <ID> 查询空岛战争数据\n'
        '/hypapi <ID> <位置> [值] 查询 Hypixel API\n'
        '/denick <Nick> Denick\n'
        '/findnick <ID> 查找 Nick\n'
        '/luck 查看幸运值 (每五分钟刷新一次)\n'
        '可能只有部分功能开启qwq\n'
        '最近账号被风控 可能会出现玩家存在但无法查到玩家的情况 一般重新查询即可',
    'qwq': lambda x: 'qwq ',
    'awa': lambda x: 'awa ',
    'qaq': lambda x: 'qaq ',
    'rwr': lambda x: 'rwr ',
    ';w;': lambda x: ';w; ',
    'uwu': lambda x: 'uwu ',
    '。。。': lambda x: 'qwq'
}


class BotAutoreply(BotBase):

    def __init__(self):
        super().__init__()
        self.bot_id = 'autoreply'

    def process(self, yqqbot, message, group_id, user_id, raw_message, settings):
        if raw_message in REPLIES:
            reply = REPLIES[raw_message](user_id)
            if reply is not None:
                yqqbot.send_group(group_id, reply)
                LOG(yqqbot, f'Replied {group_id} {user_id} {raw_message}')


bot = BotAutoreply()
