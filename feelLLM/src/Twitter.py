import asyncio
import base64
import datetime
import re

import requests
import time
import traceback
import aiohttp
import loguru
import uuid
from pydantic_settings  import BaseSettings

import queue

# from app.config import settings
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = "Bubbleai with you forever 2028-08-01 00:00:00"
    MAINNET_PROVIDER:str  = "https://eth-mainnet.g.alchemy.com/v2/AnCBrNtZeSuobFOvZFMbuG1UMIpgY6MB"
    BSC_NET_PROVIDER:str  = "https://binance.llamarpc.com"
    TEXT_NET_PROVIDER:str  = "https://eth-goerli.g.alchemy.com/v2/AixdFbFESx-T0LwJ-TY2CZPJ6HEwGj_h"
    UNISWAP_ROUTER_ADDRESS:str = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
    DB_URI: str = "root:root@192.168.1.6:3306/test"
    REDIS_URI: str = "redis://127.0.0.1:6379/0"
    UNIV3_ROUTER_ADDRESS:str = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
    UNIV2_ROUTER_ADDRESS:str = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    MINNET_WETH_ADDRESS:str = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    TEXTNET_WETH_ADDRESS:str = "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"

    REDIS_POOL_CHANNEL:str = "pool"
    REDIS_POOL_PROCESS_STATUS_CHANNEL:str = "pool_process_status"
    REDIS_USER_STATUS_CHANNEL:str = "user_status_channel"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"

    # PROXY = "http://{}:{}@{}:{}".format(pconfig['proxyUser'], pconfig['proxyPass'], pconfig['proxyHost'], pconfig['proxyPort'])
    # "https": "http://{}:{}@{}:{}".format(pconfig['proxyUser'], pconfig['proxyPass'], pconfig['proxyHost'], pconfig['proxyPort'])
    PROXY: str = "http://158.178.225.38:38080"
    proxyUser: str = "bubbleai_session-test_life-5"
    proxyPass: str = "bubbleai"
    proxyHost: str = "proxy.smartproxycn.com"
    proxyPort: str = "1000"
    PROXY_POOL: str = "http://{}:{}@{}:{}".format(
        proxyUser, proxyPass, proxyHost, proxyPort
    )


settings = Settings()



class Twitter_Stream:
    def __init__(self):
        self.cache = []
        self.headers = None
        self.cookies = None
        self.redis_lists = []
        self.twitter_id_lists = {}
        self.flag = 1
        self.queue = asyncio.Queue()  # create a new queue

        self.insert_headers = {"Content-Type": "application/json"}

        self.auth_token_lists = [
            #"e0b30411fbaa6894035a8ef906f112388d15ab40",  # 蓝v
            "cf5e49ae43aae1e9db9c26b252f98c8b59c06c6f"
        ]
        # 创建一个队列
        self.token_queue = queue.Queue()

        for auth_token in self.auth_token_lists:
            self.token_queue.put(auth_token)
        # 获取第一个蓝v
        self.auth_token = self.token_queue.get()

    async def prepare_headers2(self):
        # 从环境变量获取信息
            headers = {
                "User-Agent": os.getenv("USER_AGENT"),
                "authorization": os.getenv("AUTHORIZATION"),
            }

        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=True)
            ) as session:
                async with session.get(
                    "https://developer.twitter.com",
                    headers={"User-Agent": headers["User-Agent"]},
                    proxy=settings.PROXY_POOL
                ) as response1:
                    async with session.post(
                        "https://api.twitter.com/1.1/guest/activate.json",
                        headers=headers,
                        proxy=settings.PROXY_POOL
                    ) as response2:
                        x_guest_token = await response2.json()
                        loguru.logger.info(f"--->{x_guest_token}")
                        x_guest_token = x_guest_token.get("guest_token")
                        ct0 = response1.headers.get("Set-Cookie")
                        ct0 = re.findall(r"ct0=(.*?);", ct0)[0]
                        headers.update(
                            {
                                "Content-type": "application/json",
                                "x-guest-token": x_guest_token,
                                "x-csrf-token": ct0,
                                "x-twitter-active-user": "yes",
                                "x-twitter-auth-type": "OAuth2Session",
                                "x-twitter-client-language": "zh-cn",
                            }
                        )
                        print(self.auth_token)
                        cookies = {
                            "auth_token": self.auth_token,
                            "ct0": ct0,
                        }

                        self.headers = headers
                        self.cookies = cookies

        except Exception as e:
            loguru.logger.error(f"{traceback.format_exc()} {e}")
            return await self.prepare_headers2()

    async def parse_tweet(self):
        params = {
            "include_profile_interstitial_type": "1",
            "include_blocking": "1",
            "include_blocked_by": "1",
            "include_followed_by": "1",
            "include_want_retweets": "1",
            "include_mute_edge": "1",
            "include_can_dm": "1",
            "include_can_media_tag": "1",
            "include_ext_has_nft_avatar": "1",
            "include_ext_is_blue_verified": "1",
            "include_ext_verified_type": "1",
            "include_ext_profile_image_shape": "1",
            "skip_status": "1",
            "cards_platform": "Web-12",
            "include_cards": "1",
            "include_ext_alt_text": "true",
            "include_ext_limited_action_results": "true",
            "include_quote_count": "true",
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_ext_views": "true",
            "include_entities": "true",
            "include_user_entities": "true",
            "include_ext_media_color": "true",
            "include_ext_media_availability": "true",
            "include_ext_sensitive_media_warning": "true",
            "include_ext_trusted_friends_metadata": "true",
            "send_error_codes": "true",
            "simple_quoted_tweet": "true",
            "count": "20",
            "requestContext": "launch",
            "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl",
        }

        while True:
            try:
                timeout = aiohttp.ClientTimeout(total=8)
                loguru.logger.info(f"---->{self.headers}, {self.cookies}")
                async with aiohttp.ClientSession(
                    cookies=self.cookies, headers=self.headers, timeout=timeout
                ) as session:
                    response = await session.get(
                        url="https://twitter.com/i/api/2/notifications/all.json",
                        params=params,
                        proxy=settings.PROXY_POOL
                    )
                    if response.status == 200:
                        loguru.logger.info(f"程序正常运行,正在等待消息,目前token:{self.auth_token}")
                        text = await response.text()
                        if "Rate limit exceeded" in text:
                            loguru.logger.debug(f"{text} 重新生成请求头准备重新执行")
                        else:
                            data = await response.json()
                            tweets: dict = data["globalObjects"]["tweets"]

                            for tweet_id, tweet in tweets.items():
                                if tweet_id not in self.redis_lists:
                                    loguru.logger.info(f"新消息:{tweet_id}")
                                    self.redis_lists.append(tweet_id)

                                    try:
                                        full_text = tweet["full_text"]
                                        created_at = tweet["created_at"]
                                        user_id = tweet["user_id"]
                                        user_mentions: list = tweet["entities"][
                                            "user_mentions"
                                        ]

                                        loguru.logger.info(
                                            f"新消息:{tweet_id} {full_text} {created_at} {user_id} {user_mentions}"
                                        )
                                    except Exception as e:
                                        loguru.logger.error(
                                            f"{traceback.format_exc()} {e}"
                                        )
                                        continue

                            await asyncio.sleep(3)
            except Exception as e:
                loguru.logger.error(f"{traceback.format_exc()}")
                loguru.logger.info(f"准备重新生成请求头")
                await self.prepare_headers2()

    async def run(self):
        await self.prepare_headers2()
        await self.parse_tweet()


if __name__ == "__main__":
    mention = Twitter_Stream()
    asyncio.run(mention.run())