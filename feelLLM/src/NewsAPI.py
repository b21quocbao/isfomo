import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

def get_news(
        api_key, 
        query='Dogecoin', 
        from_days_ago=3, 
        sort_by='relevancy', 
        page_size=100, 
        page=1, 
        language=None, 
        sources=None, 
        domains=None, 
        exclude_domains=None
    ):
    """
    从 NewsAPI 获取新闻文章。

    参数:
        api_key (str): 您的 NewsAPI API 密钥。
        query (str): 搜索关键词或短语。默认值为 'Dogecoin'。
        from_days_ago (int): 从当前时间起往前推多少天作为起始日期。默认值为 3 天。
        sort_by (str): 排序方式，可选 'relevancy', 'popularity', 'publishedAt'。默认值为 'relevancy'。
        page_size (int): 每页返回的结果数量。默认值为 100，最大值为 100。
        page (int): 要获取的页码。默认值为 1。
        language (str): 2 字母 ISO-639-1 语言代码，例如 'en'。可选。
        sources (str): 以逗号分隔的新闻来源标识符列表。可选。
        domains (str): 以逗号分隔的域名列表，限制搜索范围。可选。
        exclude_domains (str): 以逗号分隔的域名列表，从结果中排除。可选。

    返回:
        list: 文章列表，如果请求失败则返回空列表。
    """
    # 当前日期和时间（UTC）
    to_date = datetime.now(timezone.utc)
    # from_days_ago 天前的日期和时间
    from_date = to_date - timedelta(days=from_days_ago)

    # 格式化日期为 ISO 8601 格式
    to_date_str = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    from_date_str = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # 新闻 API 端点
    url = 'https://newsapi.org/v2/everything'

    # 构建请求参数
    params = {
        'q': query,
        'from': from_date_str,
        'to': to_date_str,
        'sortBy': sort_by,
        'pageSize': page_size,
        'page': page,
        'apiKey': api_key
    }

    # 添加可选参数
    if language:
        params['language'] = language
    if sources:
        params['sources'] = sources
    if domains:
        params['domains'] = domains
    if exclude_domains:
        params['excludeDomains'] = exclude_domains

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)
        # 检查响应状态码
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP 错误发生: {http_err}')
        return []
    except requests.exceptions.ConnectionError as conn_err:
        print(f'连接错误发生: {conn_err}')
        return []
    except Exception as err:
        print(f'其他错误发生: {err}')
        return []

    # 解析 JSON 响应
    data = response.json()

    if data.get('status') != 'ok':
        print(f"错误: {data.get('message')}")
        return []

    total_results = data.get('totalResults', 0)
    articles = data.get('articles', [])

    # print(f"总共有 {total_results} 篇相关文章（显示第 {page} 页的 {len(articles)} 篇）\n")

    for idx, article in enumerate(articles, start=1):
        source = article.get('source', {}).get('name', 'Unknown Source')
        author = article.get('author', 'Unknown Author')
        title = article.get('title', 'No Title')
        description = article.get('description', 'No Description')
        url = article.get('url', '')
        published_at = article.get('publishedAt', 'Unknown Date')

        # print(f"文章 {idx}:")
        # print(f"来源: {source}")
        # print(f"作者: {author}")
        # print(f"标题: {title}")
        # print(f"描述: {description}")
        # print(f"链接: {url}")
        # print(f"发布时间: {published_at}")
        # print("-" * 80)

    return articles

if __name__ == "__main__":
    # 使用环境变量存储 API 密钥，提高安全性
    API_KEY = os.getenv('NEWSAPI_KEY', 'YOUR_API_KEY')  # 请确保替换为您的实际 API 密钥

    if API_KEY == 'YOUR_API_KEY' or not API_KEY:
        print("请将 'YOUR_API_KEY' 替换为您的实际 NewsAPI 密钥，或者设置环境变量 'NEWSAPI_KEY'.")
    else:
        # 示例调用，可以根据需要修改参数
        get_news(
            api_key=API_KEY,
            query='Dogecoin',
            from_days_ago=3,
            sort_by='relevancy',
            page_size=100,
            page=1,
            language='en'  # 例如，只获取英语文章
            # sources='bbc-news,techcrunch',  # 可选，指定新闻来源
            # domains='bbc.co.uk,techcrunch.com',  # 可选，限制搜索范围
            # exclude_domains='example.com'  # 可选，排除特定域名
        )
