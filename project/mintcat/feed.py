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

        # feed cat
        feed_cat_count = 0
        while cat.can_feed():
            if feed_cat_count >= 5:
                break
            try:
                if cat.can_feed():
                    cat.feed_cat()
                    feed_cat_count += 1
                    logger.info(f"养猫交易执行成功，tokenId:{token_id}, 次数:{feed_cat_count}")
                else:
                    logger.info(f"养猫交易执行失败，当前不能执行养猫交易，tokenId:{token_id}")
            except Exception as e:
                logger.info(f"养猫交易执行异常，tokenId:{token_id}, 异常信息:{e}")
            # 睡眠90s
            time.sleep(90)

        # clean cat
        # clean_cat_count = 0
        # while cat.can_clean():
        #     if clean_cat_count >= 3:
        #         break
        #     try:
        #         if cat.can_clean():
        #             cat.clean_cat()
        #             clean_cat_count += 1
        #             logger.info(f"洗猫交易执行成功，tokenId:{token_id}, 次数:{clean_cat_count}")
        #         else:
        #             logger.info(f"洗猫交易执行失败，当前不能执行养猫交易，tokenId:{token_id}")
        #     except Exception as e:
        #         logger.info(f"洗猫交易执行异常，tokenId:{token_id}, 异常信息:{e}")
        #     # 睡眠90s
        #     time.sleep(90)





