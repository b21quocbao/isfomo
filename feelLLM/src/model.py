from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import Qwen2ForCausalLM, Qwen2Tokenizer
from transformers import Qwen2Config


class CausalModelForClassification:
    def __init__(
        self,
        model_name_or_path: str,
        label_tokens: list[int],
        device_map: str = "auto",
    ) -> None:
        self.model_name_or_path: str = model_name_or_path
        self.label_tokens: list[int] = label_tokens
        self.device_map = device_map

        self.model: Qwen2ForCausalLM = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=self.model_name_or_path,
            device_map=device_map,
            trust_remote_code=True,
        )
        self.tokenizer: Qwen2Tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.model_name_or_path,
            truncation="left",
        )

    def classify(
        self,
        text: str,
    ) -> dict[int, float]:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        )
        outputs = self.model.generate(
            inputs=inputs,
            max_new_tokens=1,
        )
        logits = outputs.logits
        probs = logits

        res_probes: dict = {}
        for i, token in enumerate(self.label_tokens):
            res_probes[token] = probs[i]

        return res_probes


__all__ = ["CausalModelForClassification"]
