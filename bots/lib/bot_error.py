class BotException(Exception):
    pass

def LOG(yqqbot, x):
    x = str(x)
    yqqbot.send_group(226782263, x)
