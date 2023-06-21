import traceback
from .bot_command import BotCommand
from .bot_error import BotException, LOG
from . import utils


class BotHypixel(BotCommand):

    def __init__(self, bot_id, command, parser):
        super().__init__()
        self.bot_id = bot_id
        self.command = command
        self.parser = parser

    def run(self, yqqbot, message, group_id, user_id, raw_message, settings):
        try:
            if len(raw_message) > 1000:
                raise BotException('指令过长!')
            args = raw_message.strip().split()[1:]
            message = self.parser(args, settings, user_id, yqqbot, group_id)
            if message is not None:
                yqqbot.send_group(group_id, message)
        except Exception as err:
            if not isinstance(err, BotException):
                err = BotException('玩家不存在!')
            raise err
