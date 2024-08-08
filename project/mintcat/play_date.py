import json
import time

from eth_account import Account
from loguru import logger
from mintcat import MintCat


if __name__ == '__main__':
    with open('cat.json', 'r') as f:
        cat_infos = json.load(f)

    for cat_info in cat_infos:
        env = cat_info['env']
        logger.info(f"开始执行MintCat交易程序，正在执行环境:{env}")
        private_key = cat_info['private_key']
        address = cat_info['address']
        token_id = cat_info['token_id']
        account = Account.from_key(private_key)
        # 创建cat实例
        cat = MintCat(address, private_key, token_id)
        canLevelUp = cat.can_level_up()
        if canLevelUp:
            cat.level_up()
            logger.info("Level up complete")

        # 约会
        play_dates_count = 0
        while cat.can_play():
            canLevelUp = cat.can_level_up()
            if play_dates_count >= 5:
                break
            # 发起邀请
            friends = cat_info['friends']
            for friend in friends:
                if play_dates_count >= 5:
                    break
                try:
                    cat.invite_cat_for_playing(friend)
                    logger.info(f"邀请朋友执行成功, friend:{friend}")
                    play_dates_count += 1
                    time.sleep(60)
                except Exception as e:
                    logger.error(f"invite cat for playing exception:{e}")





