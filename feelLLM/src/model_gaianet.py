import requests
import random

from transformers import AutoTokenizer


class GaiaNetCausalModelForClassification:
    def __init__(
        self,
        model_name: str | None = None,
        api_url: str = "https://0x9b829bf1e151def03532ab355cdfe5cee001f4b0.us.gaianet.network/v1/chat/completions",
    ):
        """GaiaNetCausalModelForClassification
        Args:

        - `model_name`: name of the LLM
        - `api_url`: OpenAI compatiable API for GaiaNet node

        """

        self.model_name: str | None = model_name
        self.api_url: str = api_url

    def get_response(self, messages: list):
        data = {
            "messages": messages,
        }
        response = requests.post(self.api_url, json=data)
        return response

    def list_to_cot_prompt(self) -> str:
        choices_cot: list[str] = [
            "If the external info will likely to result in a price increase, type: good",
            "If the external info will likely to result in a price decrease, type: bad",
            "If the external info will likely to result in no price change, type: neutral",
        ]

        random.shuffle(choices_cot)

        return "\n\n".join(choices_cot)

    def prompt(
        self,
        info_text: str,
        asset_name: str,
        asset_info: str,
    ) -> str:
        # info_text: str = """@UberFacts on Twitter 2020-07-07 00:00:00

        # Elon Musk is predicted to become the world's first trillionaire, thanks to SpaceX.

        # @elonmusk Replies to @UberFacts on Twitter 2020-07-07 00:00:00

        # *In dogecoin!"""
        # asset_name: str = "DOGE coin"
        # asset_info: str = "DOGE coin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of DOGE coin has been known to be volatile and is often influenced by social media trends and celebrity endorsements."
        prompt: str = f"""The following is external information:

        ---

        {info_text}

        ---

        You need to class the external information in terms of price for {asset_name}. For your information, {asset_info}.

        {self.list_to_cot_prompt()}

        Based on the given external info. Decide it's impact on the price of {asset_name}."""

        return prompt

    def classify(
        self,
        prompt: str,
    ) -> tuple[int, str]:
        response = self.get_response(
            [
                {
                    "role": "system",
                    "content": "You are only allowed return one words each time. The response word should be one of good, bad, neutral.",
                },
                {"role": "user", "content": f"{prompt}"},
            ]
        )

        # if OK 200
        if response.status_code == 200:
            response_text = (
                response.json()
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            # print(f"response_text: {response_text}")
            first_word = response_text.split()[0].lower() if response_text else ""
            if first_word in ["good", "bad", "neutral"]:
                return response.status_code, first_word

        return response.status_code, "neutral"


__all__ = ["GaiaNetCausalModelForClassification"]
