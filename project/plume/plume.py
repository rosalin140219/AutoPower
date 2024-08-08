import json
import random
import time

from loguru import logger

from project.plume.ambient.ambient import Ambient
from project.plume.arc.arc import PlumeArc
from project.plume.checkin.checkin import Checkin
from project.plume.cultured.cultured import Cultured
from project.plume.faucet.faucet import Faucet
from project.plume.kuma.kuma import Kuma
from project.plume.landshare.landshare import LandShare
from project.plume.neststaking.neststaking import NestStaking

if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)

    for wallet in wallets:
        env = wallet['env']
        logger.info(f"正在执行环境:{env}的签到")
        address = wallet['address']
        private_key = wallet['private_key']
        proxy = wallet['proxy']

        # 签到
        try:
            plume = Checkin(address, private_key, proxy)
            plume.check_in()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}签到失败，失败原因:{e}")

        # 领水
        faucet = Faucet(address, private_key, proxy)
        try:
            faucet.faucet("ETH")
        except Exception as e:
            logger.error(f"环境:{wallet['env']}领水ETH失败，失败原因:{e}")

        time.sleep(10)
        try:
            faucet.faucet("GOON")
        except Exception as e:
            logger.error(f"环境:{wallet['env']}领水GOON失败，失败原因:{e}")

        # ambient
        try:
            ambient = Ambient(address, private_key)
            ambient.swap()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行swap失败，失败原因:{e}")

        # arc
        try:
            arc = PlumeArc(address, private_key)
            arc.create_token()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行ARC失败，失败原因:{e}")

        # cultured
        try:
            cultured = Cultured(address, private_key)
            predict_types = ['crypto', 'forex']
            cultured.predict_price_movement(random.choice(predict_types))
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行Cultured预测失败，失败原因:{e}")

        # kuma
        kuma = Kuma(address, private_key)
        try:
            tx = kuma.mint_aick()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行MintAICK失败，失败原因:{e}")

        time.sleep(60)
        try:
            token_id_list = kuma.get_all_user_kuma_bond_tokens()
            if len(token_id_list) > 0:
                for token_id in token_id_list:
                    time.sleep(30)
                    kuma.approve(int(token_id))
                    time.sleep(30)
                    kuma.sell_bond(int(token_id))
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行SellBond失败，失败原因:{e}")

        # landshare
        land_share = LandShare(address, private_key)
        try:
            land_share.approve_gnusd()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:approve_gnUsd失败，失败原因:{e}")
        time.sleep(10)

        try:
            land_share.swap()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:swapLand失败，失败原因:{e}")
        time.sleep(10)

        try:
            land_share.approve_land()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:approveLand失败，失败原因:{e}")

        time.sleep(10)
        try:
            land_share.deposit()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:deposit失败，失败原因:{e}")

        # neststaking
        nest = NestStaking(address, private_key)
        try:
            nest.approve_gnusd(100000000000000000000)
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行staking:approve失败，失败原因:{e}")
        time.sleep(10)

        try:
            nest.stake(100000000000000000000)
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行staking:stake失败，失败原因:{e}")