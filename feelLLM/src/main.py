from .model import CausalModelForClassification
from transformers import AutoTokenizer
import random

model_name: str = "models/Qwen2-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path=model_name,
    truncation="left",
)


def list_to_cot_prompt() -> str:
    choices_cot: list[str] = [
        "If it has postive impact, the prediction should be:\n\nThe impact of external info on the asset is postive",
        "If it has negative impact, the prediction should be:\n\nThe impact of external info on the asset is negative",
        "If it has neutral impact, the prediction should be:\n\nThe impact of external info on the asset is neutral",
    ]

    random.shuffle(choices_cot)

    return "\n\n".join(choices_cot)


info_text: str = ""
asset_name: str = "asset"
asset_info: str = "asset_info"
prompt: str = f"""The following is external information:

---

{info_text}

---

You need to decide if the external information has a positive, negative or neutral impact on the asset: {asset_name}. For your information, {asset_info}.

{list_to_cot_prompt()}

Based on the given external info.

The impact of external info on the asset is """


model: CausalModelForClassification = CausalModelForClassification(
    model_name_or_path=model_name, label_tokens=[]
)
