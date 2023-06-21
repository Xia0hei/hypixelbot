import os
import sys
import re
import importlib
import json
import traceback
import yqqbot
import threading
from bots.lib.bot_error import LOG


BOTS_DIR = 'bots'
SETTINGS_FILE = 'bot_loader.json'
RE_MODULE = re.compile('[A-Za-z_][A-Za-z0-9_]*')


bot_list = {}
settings = {
    'global': {
        'blacklist': [],
        'whitelist': [],
        'admins': [],
        'api_cdn': False
    },
    'base': {
        'enabled': True,
        'listmode': 'blacklist',
        'blacklist': [],
        'whitelist': []
    },
    'bots': {}
}


def create_dir():
    os.chdir(os.path.dirname(__file__))
    try:
        os.mkdir(BOTS_DIR)
    except Exception:
        pass


def load_settings():
    global settings
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as fr:
                settings = json.loads(fr.read())
    except Exception as err:
        print(f'An error occurred while loading settings!', err)


def save_settings():
    try:
        with open(SETTINGS_FILE, 'w') as fw:
            fw.write(json.dumps(settings))
    except Exception as err:
        print(f'An error occurred while saving settings!', err)


def load_bot(bot):
    bot_list[bot.bot_id] = bot
    if bot.bot_id not in settings['bots']:
        settings['bots'][bot.bot_id] = json.loads(json.dumps(settings['base']))


def load_bots():
    file_list = os.listdir(BOTS_DIR)
    for file_name in file_list:
        if file_name.endswith('.py'):
            if os.path.isfile(f'{BOTS_DIR}/{file_name}'):
                module_name = file_name[:-3]
                if RE_MODULE.match(module_name):
                    print(f'Loading bot <{module_name}> ...')
                    try:
                        load_bot(importlib.import_module(
                            f'{BOTS_DIR}.{module_name}').bot)
                    except Exception as err:
                        print(
                            f'An error occurred while loading bot <{module_name}> !', err)


def processor(message):
    if message['post_type'] == 'message':
        if message['message_type'] == 'group':
            group_id = message['group_id']
            user_id = message['user_id']
            raw_message = message['raw_message']
            for name, bot in bot_list.items():
                if settings['bots'][name]['enabled']:
                    blacklist = settings['global']['blacklist'] + \
                        settings['bots'][name]['blacklist']
                    whitelist = settings['global']['whitelist'] + \
                        settings['bots'][name]['whitelist']
                    if group_id in blacklist:
                        continue
                    elif group_id not in whitelist and settings['bots'][name]['listmode'] == 'whitelist':
                        continue
                    thread = threading.Thread(target=bot.process, args=(
                        yqqbot, message, group_id, user_id, raw_message, settings))
                    thread.daemon = True
                    thread.start()


def start_bots():
    yqqbot.start_listener(processor)


def run_command(args):
    print('Command:', *args)
    output = ''
    if len(args) == 0:
        pass
    elif args[0] == 'q':
        LOG(yqqbot, 'Shutdown!')
        os._exit(0)
    elif args[0] == 'l':
        for name, bot in bot_list.items():
            output += ('On  ' if settings['bots'][name]['enabled'] else 'Off ') +\
                    ('BL ' if settings['bots'][name]['listmode'] == 'blacklist' else 'WL ') + name + '\n'
    elif args[0] == 'wga':
        lst = settings['global']['whitelist']
        if args[1] not in lst:
            lst.append(int(args[1]))
        output += 'Added ' + args[1] + ' to global whitelist!'
    elif args[0] == 'bga':
        lst = settings['global']['blacklist']
        if args[1] not in lst:
            lst.append(int(args[1]))
        output += 'Added ' + args[1] + ' to global blacklist!'
    elif args[0] == 'wgr':
        settings['global']['whitelist'].remove(int(args[1]))
        output += 'Removed ' + args[1] + ' from global whitelist!'
    elif args[0] == 'bgr':
        settings['global']['blacklist'].remove(int(args[1]))
        output += 'Removed ' + args[1] + ' from global blacklist!'
    elif args[0] == 'wla':
        lst = settings['bots'][args[1]]['whitelist']
        if args[1] not in lst:
            lst.append(int(args[2]))
        output += 'Added ' + args[2] + f' to bot <{args[1]}> whitelist!'
    elif args[0] == 'bla':
        lst = settings['bots'][args[1]]['blacklist']
        if args[1] not in lst:
            lst.append(int(args[2]))
        output += 'Added ' + args[2] + f' to bot <{args[1]}> blacklist!'
    elif args[0] == 'wlr':
        settings['bots'][args[1]]['whitelist'].remove(int(args[2]))
        output += 'Removed ' + args[2] + f' from bot <{args[1]}> whitelist!'
    elif args[0] == 'blr':
        settings['bots'][args[1]]['blacklist'].remove(int(args[2]))
        output += 'Removed ' + args[2] + f' from bot <{args[1]}> blacklist!'
    elif args[0] == 'e':
        settings['bots'][args[1]]['enabled'] = True
        output += f'Enabled bot <{args[1]}> !'
    elif args[0] == 'd':
        settings['bots'][args[1]]['enabled'] = False
        output += f'Disabled bot <{args[1]}> !'
    elif args[0] == 'w':
        settings['bots'][args[1]]['listmode'] = 'whitelist'
        output += f'Set bot <{args[1]}> to whitelist mode!'
    elif args[0] == 'b':
        settings['bots'][args[1]]['enabled'] = 'blacklist'
        output += f'Set bot <{args[1]}> to blacklist mode!'
    elif args[0] == 'lwg':
        for group in settings['global']['whitelist']:
            output += str(group) + '\n'
    elif args[0] == 'lbg':
        for group in settings['global']['blacklist']:
            output += str(group) + '\n'
    elif args[0] == 'lwl':
        for group in settings['bots'][args[1]]['whitelist']:
            output += str(group) + '\n'
    elif args[0] == 'lbl':
        for group in settings['bots'][args[1]]['blacklist']:
            output += str(group) + '\n'
    elif args[0] == 's':
        group_id = int(args[1])
        user_id = int(args[2])
        raw_message = ' '.join(args[3:])
        message = {
            'post_type': 'message',
            'message_type': 'group',
            'group_id': group_id,
            'user_id': user_id,
            'raw_message': raw_message
        }
        processor(message)
        output += f'Processing message from group {group_id} from {user_id}!'
    elif args[0] == 'ss':
        group_id = int(args[1])
        user_id = int(args[2])
        raw_message = ' '.join(args[3:])
        message = {
            'post_type': 'message',
            'message_type': 'group',
            'group_id': group_id,
            'user_id': user_id,
            'raw_message': raw_message
        }
        yqqbot.send_group(group_id, raw_message)
        processor(message)
        output += f'Sent message to group {group_id} as {user_id}!'
    elif args[0] == 'cdn':
        cdn = not settings['global']['api_cdn']
        settings['global']['api_cdn'] = cdn
        output += f'Switched CDN {"on" if cdn else "off"}!'
    elif args[0] == 'op':
        settings['global']['admins'].append(int(args[1]))
        output += f'Opped {args[1]}!'
    elif args[0] == 'deop':
        settings['global']['admins'].remove(int(args[1]))
        output += f'Deopped {args[1]}!'
    print(output)
    LOG(yqqbot, 'Command: ' + ' '.join(args) + '\n' + output)
    return output


def command_loop():
    global settings
    while True:
        try:
            command = input('>>> ').strip()
            args = command.split()
            run_command(args)
            save_settings()
        except Exception as err:
            LOG(yqqbot, traceback.format_exc())
            print('An error occured!', err)


def main(args):
    create_dir()
    load_settings()
    load_bots()
    save_settings()
    start_bots()
    LOG(yqqbot, 'Startup!')
    yqqbot.set_loader(run_command)
    command_loop()


if __name__ == '__main__':
    main(sys.argv)
