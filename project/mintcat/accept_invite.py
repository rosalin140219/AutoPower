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
            if play_dates_count >= 10:
                break
            # 接受邀请
            invite_list = cat.get_play_invites_list()
            if invite_list:
                for invite in invite_list:
                    try:
                        invite_id = invite[0]
                        cat.accept_play_date(invite_id)
                        logger.info(f"接受邀请交易执行成功，invitee:{invite_id}")
                        time.sleep(70)
                        play_dates_count += 1
                    except Exception as e:
                        logger.error(f"接受邀请交易执行异常，invitee:{invite_id}，异常:{e}")
            else:
                break






