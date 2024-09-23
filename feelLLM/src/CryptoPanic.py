import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

def fetch_dogecoin_news(auth_token, currency='DOGE', filter_option='all', public='true'):
    """
    获取 Dogecoin 相关新闻

    :param auth_token: API 认证令牌
    :param currency: 查询的加密货币（默认是 'DOGE'）
    :param filter_option: 过滤条件（默认是 'all'）
    :param public: 是否允许公共访问（默认是 'true'）
    :return: 返回包含所有 Dogecoin 新闻的列表和包含 'Elon Musk' 新闻的列表
    """
    url = 'https://cryptopanic.com/api/v1/posts/'
    params = {
        'auth_token': auth_token,
        'currencies': currency,
        'filter': filter_option,
        'public': public
    }

    # 发送 GET 请求
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data.get('results', [])
        
        # 输出所有获取到的新闻
        print("=== 所有 Dogecoin 相关新闻 ===\n")
        for post in posts:
            print(f"标题: {post.get('title')}")
            print(f"来源: {post.get('source', {}).get('title')}")
            print(f"发布时间: {post.get('published_at')}")
            print(f"链接: {post.get('url')}\n")

        # 筛选包含 “Elon Musk” 的新闻
        elon_related_posts = []
        for post in posts:
            title = post.get('title', '').lower()
            content = post.get('content', '').lower()
            if 'elon musk' in title or 'elon musk' in content:
                elon_related_posts.append(post)

        # 输出筛选后的新闻
        print("=== 包含 'Elon Musk' 的 Dogecoin 新闻 ===\n")
        for post in elon_related_posts:
            print(f"标题: {post.get('title')}")
            print(f"来源: {post.get('source', {}).get('title')}")
            print(f"发布时间: {post.get('published_at')}")
            print(f"链接: {post.get('url')}\n")
        
        return posts, elon_related_posts  # 返回所有新闻和包含 'Elon Musk' 的新闻
    else:
        print(f"API请求失败，状态码: {response.status_code}")
        return None, None

# 使用函数
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
if AUTH_TOKEN:
    fetch_dogecoin_news(AUTH_TOKEN)
else:
    print("请在 .env 文件中设置 'AUTH_TOKEN'。")
