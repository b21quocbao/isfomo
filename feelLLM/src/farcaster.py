import requests
import urllib.parse
from datetime import datetime, timedelta

def search_casts(
    base_url="https://searchcaster.xyz",
    text=None,
    count=200,  # 最大查询数量设为200
    engagement=None,
    merkleRoot=None,
    page=1,
    username=None
):
    """
    查询 Searchcaster API 的 /api/search 端点。

    参数：
        base_url (str): Searchcaster 的基础 URL。
        text (str): 按文本内容搜索（不区分大小写）。
        count (int): 返回的消息数量（最大 200，默认 200）。
        engagement (str): 根据互动指标排序。选项包括 "reactions", "recasts", "replies", "watches"。
        merkleRoot (str): 消息的唯一标识符，返回该消息及其所有直接回复。（覆盖所有其他参数）
        page (int): 相对于 count 的偏移页数。
        username (str): 返回特定用户的所有消息，包括回复。

    返回：
        dict: JSON 格式的响应数据。
    """
    endpoint = "/api/search"
    url = urllib.parse.urljoin(base_url, endpoint)
    
    params = {}
    
    if text:
        params['text'] = text
    if count:
        params['count'] = min(count, 200)  # 确保 count 不超过 200
    if engagement:
        if engagement in ["reactions", "recasts", "replies", "watches"]:
            params['engagement'] = engagement
        else:
            raise ValueError("engagement 参数无效。有效选项为 'reactions', 'recasts', 'replies', 'watches'")
    if merkleRoot:
        params['merkleRoot'] = merkleRoot
    if page:
        params['page'] = page
    if username:
        params['username'] = username
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def filter_casts_by_time(casts, hours):
    """
    根据指定的时间范围（小时）筛选消息。

    参数：
        casts (list): 从 API 获取的消息列表。
        hours (int): 查询过去多少小时内的消息。

    返回：
        list: 过滤后的消息列表。
    """
    # 计算指定小时数前的时间戳（毫秒）
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    time_threshold_timestamp = int(time_threshold.timestamp() * 1000)
    
    filtered_casts = []
    
    for cast in casts:
        published_at = cast.get('body', {}).get('publishedAt', 0)
        if published_at >= time_threshold_timestamp:
            filtered_casts.append({
                'username': cast.get('body', {}).get('username', '未知用户'),
                'published_time': datetime.fromtimestamp(published_at / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                'text': cast.get('body', {}).get('data', {}).get('text', '')
            })
    
    return filtered_casts

def get_filtered_casts(
    text,
    hours=168,       # 默认查询过去一周（168小时）
    limit=30,        # 默认返回30条
    engagement=None,
    username=None,
    base_url="https://searchcaster.xyz"
):
    """
    获取符合时间范围的消息。

    参数：
        text (str): 按文本内容搜索（不区分大小写）。
        hours (int): 查询过去多少小时内的消息。
        limit (int): 返回的消息数量上限。
        engagement (str, optional): 根据互动指标排序。选项包括 "reactions", "recasts", "replies", "watches"。
        username (str, optional): 返回特定用户的所有消息，包括回复。
        base_url (str): Searchcaster 的基础 URL。

    返回：
        list: 过滤后的消息列表，每条消息包含用户名、发布时间和内容。
    """
    # 首先查询最多200条消息
    casts_data = search_casts(
        base_url=base_url,
        text=text,
        count=200,
        engagement=engagement,
        username=username
    )
    
    if casts_data and 'casts' in casts_data:
        casts = casts_data['casts']
        # 过滤指定时间范围内的消息
        filtered_casts = filter_casts_by_time(casts, hours)
        # 返回前limit条消息
        return filtered_casts[:limit]
    else:
        print("响应中不包含 'casts' 键或查询失败。")
        return []