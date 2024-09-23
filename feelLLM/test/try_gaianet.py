# from src.model_gaianet import GaiaNetCausalModelForClassification
from src.model_gaianet import GaiaNetCausalModelForClassification


info_text: str = """@UberFacts on Twitter 2020-07-07 00:00:00

Elon Musk is predicted to become the world's first trillionaire, thanks to SpaceX.

@elonmusk Replies to @UberFacts on Twitter 2020-07-07 00:00:00

*In dogecoin!"""
asset_name: str = "DOGE coin"
asset_info: str = "DOGE coin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of DOGE coin has been known to be volatile and is often influenced by social media trends and celebrity endorsements."

model: GaiaNetCausalModelForClassification = GaiaNetCausalModelForClassification()

prompt: str = model.prompt(
    info_text=info_text,
    asset_name=asset_name,
    asset_info=asset_info,
)

print(f"prompt: {prompt}")

stat, resp = model.classify(prompt)

print(f"stat: {stat}")
print(f"resp: {resp}")
