from .lib.bot_hypixel import BotHypixel
from .lib.bot_error import BotException
from .lib import langs
from .lib import hyp_player

FAVORITE_MAP = {
    'null': '空',
    'wool': '羊毛',
    'hardened_clay': '粘土',
    'blast-proof_glass': '玻璃',
    'end_stone': '末地石',
    'ladder': '梯子',
    'oak_wood_planks': '木板',
    'obsidian': '黑曜石',
    'stone_sword': '石剑',
    'iron_sword': '铁剑',
    'diamond_sword': '钻石剑',
    'stick_(knockback_i)': '击退棒',
    'chainmail_boots': '锁链套',
    'iron_boots': '铁套',
    'diamond_boots': '钻石套',
    'shears': '剪刀',
    'wooden_pickaxe': '镐',
    'wooden_axe': '斧',
    'arrow': '箭',
    'bow': '弓',
    'bow_(power_i)': '力量弓',
    'bow_(power_i__punch_i)': '冲击弓',
    'speed_ii_potion_(45_seconds)': '速度',
    'jump_v_potion_(45_seconds)': '跳跃',
    'invisibility_potion_(30_seconds)': '隐身',
    'golden_apple': '金苹果',
    'bedbug': '床虱',
    'dream_defender': '铁傀儡',
    'fireball': '火球',
    'tnt': 'TNT',
    'ender_pearl': '珍珠',
    'water_bucket': '水桶',
    'bridge_egg': '搭桥蛋',
    'magic_milk': '牛奶',
    'sponge': '海绵',
    'compact_pop-up_tower': '速建塔',
    'magnum': '马格南手枪',
    'rifle': '步枪',
    'smg': 'SMG',
    'not-a-flamethrower': '不是喷火器',
    'shotgun': '霰弹枪'
}


class BotFavorites(BotHypixel):

    def __init__(self):
        super().__init__()
        self.bot_id = 'favorites'
        self.command = 'bwfav'

    def parse(self, yqqbot, group_id, user_id, args, settings):
        if len(args) != 1:
            raise BotException(langs.ERROR_ARGUMENT)
        try:
            player = hyp_player.get_player(args[0])
            favorites = player['stats']['Bedwars']['favourites_2']
            message = hyp_player.get_name(player) + ' 的快速购买:'
            part = ''
            for i, favorite in enumerate(favorites.split(',')[:21]):
                part += FAVORITE_MAP.get(favorite, '???') + ' '
                if i % 7 == 6:
                    message += f'\n[{part.strip()}]'
                    part = ''
            yqqbot.send_group(group_id, message)
        except Exception as err:
            raise BotException(langs.ERROR_QUERY)


bot = BotFavorites()
