import json
from farcaster import get_filtered_casts  # 从farcaster导入函数
from try_gaianet import classify_asset_with_gaianet  # 从try_gaianet导入函数

def query_and_classify_individual(
    search_text="dogecoin",
    hours=24,  # 默认查询过去24小时的消息
    limit=5,   # 默认返回5条消息
    asset_name="DOGE coin",
    asset_info="DOGE coin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of DOGE coin has been known to be volatile and is often influenced by social media trends and celebrity endorsements."
):
    """
    从farcaster获取指定内容的消息，并将每条消息分别传递给GaiaNetCausalModel进行分析。

    参数:
        search_text (str): 按文本内容搜索
        hours (int): 查询过去多少小时内的消息
        limit (int): 返回的消息数量上限
        asset_name (str): 要分析的资产名称
        asset_info (str): 资产的描述信息
    
    返回:
        list: 包含每条消息内容和分类结果的字典列表
    """
    # 1. 从farcaster.py获取符合条件的消息
    filtered_casts = get_filtered_casts(text=search_text, hours=hours, limit=limit)

    results = []

    # 2. 遍历每条获取到的消息
    for cast in filtered_casts:
        # 获取消息内容
        info_text = f"{cast['username']} at {cast['published_time']}: {cast['text']}"
        
        # 使用try_gaianet的classify_asset_with_gaianet函数进行分类
        result = classify_asset_with_gaianet(info_text, asset_name, asset_info)
        
        # 只保留消息内容和分类结果(resp)
        results.append({
            "message": info_text,
            "resp": result["resp"]
        })

    return results

# 测试调用
if __name__ == "__main__":
    # 示例数据
    search_text = "Musk"
    hours = 256
    limit = 200
    asset_name = "DOGE coin"
    asset_info = "DOGE coin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of DOGE coin has been known to be volatile and is often influenced by social media trends and celebrity endorsements."

    # 调用query_and_classify_individual函数
    analysis_results = query_and_classify_individual(search_text, hours, limit, asset_name, asset_info)
    
    # 以JSON格式打印结果，仅包括消息内容和resp
    print(json.dumps(analysis_results, indent=4, ensure_ascii=False))

# # 测试调用
# if __name__ == "__main__":
#     # 示例数据
#     search_text = "trump"  # 将搜索词替换为“trumpcoin”
#     hours = 128
#     limit = 50
#     asset_name = "TRUMP coin"  # 将资产名称替换为“TRUMP coin”
#     asset_info = "TRUMP coin is a cryptocurrency named after the former US President Donald Trump. It was created to support the Trump administration and its supporters, representing a political stance. Like many cryptocurrencies, its price can be volatile and influenced by social media trends and political endorsements."

#     # 调用query_and_classify_individual函数
#     analysis_results = query_and_classify_individual(search_text, hours, limit, asset_name, asset_info)
    
#     # 以JSON格式打印结果，仅包括消息内容和resp
#     print(json.dumps(analysis_results, indent=4, ensure_ascii=False))
