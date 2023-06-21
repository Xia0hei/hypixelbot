from .bot_base import BotBase
from .cooldown import Cooldown
from .bot_error import BotException, LOG
import traceback


class BotCommand(BotBase):

    def __init__(self):
        super().__init__()
        self.command = ''
        self.cooldown = Cooldown(1.0)

    def run(self, yqqbot, message, group_id, user_id, raw_message, settings):
        pass

    def process(self, yqqbot, message, group_id, user_id, raw_message, settings):
        if raw_message.startswith(f'/{self.command} ') or raw_message == f'/{self.command}':
            try:
                self.cooldown.wait()
                self.run(yqqbot, message, group_id, user_id, raw_message, settings)
                LOG(yqqbot, f'OK {group_id} {user_id} {raw_message}')
            except Exception as err:
                LOG(yqqbot, f'Error {group_id} {user_id} {raw_message}\n' + traceback.format_exc())
                yqqbot.send_group(group_id, f'[CQ:at,qq={user_id}] {err}')
