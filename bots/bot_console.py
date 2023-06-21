from itertools import groupby
from .lib.bot_hypixel import BotHypixel
from .lib import langs
from .lib.utils import *


def parser(args, settings, user_id, yqqbot, group_id):
    if user_id in settings['global']['admins']:
        yqqbot.send_group(group_id, 'Command Run: ' + ' '.join(args))
        output = yqqbot.BOT_LOADER(args)
        yqqbot.send_group(group_id, 'Command OK: ' + ' '.join(args) + '\n' + output)


bot = BotHypixel('console', '/', parser)
