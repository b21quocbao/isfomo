import json
from model_gaianet import GaiaNetCausalModelForClassification

def classify_asset_with_gaianet(info_text: str, asset_name: str, asset_info: str) -> dict:
    """
    使用GaiaNetCausalModelForClassification对给定的信息、资产名称和资产信息进行分类，并以JSON格式返回结果。

    参数:
        info_text (str): 包含信息内容的文本
        asset_name (str): 资产名称
        asset_info (str): 资产的描述信息

    返回:
        dict: 包含 prompt, stat, resp 的结果字典
    """
    # 初始化模型
    model = GaiaNetCausalModelForClassification()

    # 生成模型的prompt
    prompt = model.prompt(
        info_text=info_text,
        asset_name=asset_name,
        asset_info=asset_info,
    )

    # 使用模型进行分类
    stat, resp = model.classify(prompt)

    # 将结果打包成JSON格式
    result = {
        "prompt": prompt,
        "stat": stat,
        "resp": resp
    }

    return result

# 测试函数
if __name__ == "__main__":
    # 示例数据
    info_text = """@UberFacts on Twitter 2020-07-07 00:00:00

    Elon Musk is predicted to become the world's first trillionaire, thanks to SpaceX.

    @elonmusk Replies to @UberFacts on Twitter 2020-07-07 00:00:00

    *In dogecoin!"""
    
    asset_name = "DOGE coin"
    asset_info = "DOGE coin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of DOGE coin has been known to be volatile and is often influenced by social media trends and celebrity endorsements."

    # 调用函数
    result = classify_asset_with_gaianet(info_text, asset_name, asset_info)
    
    # 将结果以JSON格式打印
    print(json.dumps(result, indent=4, ensure_ascii=False))
